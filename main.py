import math
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QTabWidget, \
    QLabel, QGraphicsScene, QGraphicsView, QGraphicsWidget, QGraphicsPixmapItem, QGraphicsTextItem, \
    QGraphicsLinearLayout, QGraphicsProxyWidget, QGraphicsRectItem, QGraphicsItem, QGraphicsLineItem, QTableWidget, \
    QTableWidgetItem, QTableView, QAbstractItemView, QHeaderView, QHBoxLayout, QSizePolicy, QGridLayout, QFrame, \
    QGraphicsSceneMouseEvent, QGraphicsObject, QGraphicsDropShadowEffect, QGraphicsRectItem, QGraphicsTextItem, \
    QTextBrowser, QStyledItemDelegate, QPushButton
from PyQt5.QtGui import QPixmap, QIcon, QColor, QFont, QPen, QPainterPath, QStandardItem, QStandardItemModel, QBrush, \
    QLinearGradient, QTextCharFormat, QTextCursor, QTextFrameFormat

from PyQt5.QtCore import Qt, QPointF, pyqtSignal, QRectF, QObject, QVariant, QSize, QRect
import sys
from PyQt5.QtGui import QTextCharFormat, QColor

from PyQt5.uic.properties import QtGui
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas

from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from extract_data import teams
from stages import group_stage, finals, player_stats
from match_report import WorldCup

class IntroScreen(QWidget):
    def __init__(self, cricket_world_cup):
        super().__init__()

        self.cricket_world_cup = cricket_world_cup

        # Layouts
        main_layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        # Widgets
        title_label = QLabel("<h1>Welcome to ICC World Cup 2023</h1>")
        start_button = QPushButton("Start Simulation")
        image_label = QLabel()

        # Load image
        image_path = "data/trophies/Trophy2.jfif"  # Provide the correct path to your image
        pixmap = QPixmap(image_path).scaledToWidth(350)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)


        # Styling
        self.setStyleSheet("""
            background-color: #222222;
            color: #303030;
            font-family: 'Arial', sans-serif;
        """)

        title_label.setStyleSheet("color: #3498DB;")

        start_button.setStyleSheet("""
            background-color: #3498DB;
            color: #ECF0F1;
            font-size: 16px;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
        """)

        # Connect signals
        start_button.clicked.connect(self.start_simulation)

        # Add widgets to layouts
        button_layout.addWidget(start_button)

        main_layout.addWidget(title_label)
        main_layout.addWidget(image_label)  # Add the image label to the layout
        main_layout.addLayout(button_layout)

        self.resize(600, 400)

        self.setLayout(main_layout)

    def start_simulation(self):
        # Switch to the CricketWorldCup widget
        self.cricket_world_cup.show()
        self.close()

def get_team_flag(team):
    flag_path = f"data/flags/{team.name}.png"
    flag_pixmap = QPixmap(flag_path).scaledToWidth(30)
    return flag_pixmap

class CricketWorldCup(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ICC World Cup 2023")
        self.resize(700, 535)

        # Create the tab widget
        tab_widget = QTabWidget(self)
        self.setCentralWidget(tab_widget)

        # Set up tabs
        self.setup_table_tab(tab_widget)
        self.setup_knockout_tab(tab_widget)
        self.setup_player_stats_tab(tab_widget)
        self.setup_matches_tab(tab_widget)

        tab_sizes = {
            'Table': (690, 637),
            'Knockout Tree': (1000, 650),
            'Player Stats': (1250, 900),
            'Matches': (1250, 900)
        }

        # Set the initial size based on the first tab
        initial_tab_name = tab_widget.tabText(0)
        initial_tab_size = tab_sizes.get(initial_tab_name, (700, 535))  # Default to the original size
        self.resize(*initial_tab_size)

        # Center the window on the screen
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y-50)

        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

        tab_widget.currentChanged.connect(lambda index: self.adjustWindowSize(index, tab_sizes))

    def adjustWindowSize(self, index, tab_sizes):
        current_tab_name = self.centralWidget().tabText(index)

        tab_size = tab_sizes.get(current_tab_name, (1000, 1000))

        self.resize(*tab_size)

        # Center the window on the screen
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y-50)

    def setup_table_tab(self, tab_widget):
        # Create a QStandardItemModel
        model = QStandardItemModel()
        model.setColumnCount(6)
        model.setHorizontalHeaderLabels(['Team', 'Played', 'Won', 'Lost', 'Points', 'NRR'])

        # Generate fixtures and calculate NRR for teams
        group_stage(teams)
        for t in teams:
            t.calc_nrr()
        ranked_teams = sorted(teams, key=lambda x: (x.points, x.NRR), reverse=True)

        # Populate the model with data
        for position, team in enumerate(ranked_teams, start=1):
            flag_pixmap = get_team_flag(team).scaledToWidth(35)
            formatted_nrr = "{:.2f}".format(team.NRR)

            item = [QStandardItem(f"{team.name}"), QStandardItem(str(team.matches_played)),
                    QStandardItem(str(team.matches_won)), QStandardItem(str(team.matches_lost)),
                    QStandardItem(str(team.points)), QStandardItem(formatted_nrr)]

            for i, col_item in enumerate(item):
                # Add a subtle green shade before the position number for the top 4 teams
                if position <= 4:
                    col_item.setBackground(QColor("#0FA23B"))

                # Center align numeric values
                col_item.setTextAlignment(Qt.AlignCenter)

                # Set item data
                model.setItem(position - 1, i, col_item)

            # Set the flag pixmap directly to the item
            model.item(position - 1, 0).setData(flag_pixmap, Qt.DecorationRole)

        # Create a QTableView
        table_view = QTableView()
        table_view.setModel(model)

        # Set column widths and other styling
        column_widths = [170, 80, 80, 80, 80]
        for col, width in enumerate(column_widths):
            table_view.setColumnWidth(col, width)

        font = QFont()
        font.setPointSize(10)
        table_view.setFont(font)

        row_height = 55
        table_view.verticalHeader().setDefaultSectionSize(row_height)

        # Header properties
        header = table_view.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Fixed)

        # Apply styles using QSS
        table_view.setStyleSheet("""
            QHeaderView::section {
                background-color: #303030;  /* Light black / matte black */
                color: white;
                font-weight: bold;
                padding: 5px;
            }
            QTableView {
                background-color: #383838;  /* Slightly lighter matte black */
                selection-background-color: #3498db;
                selection-color: white;
                alternate-background-color: #303030;  /* Same as section background */
                color: white;
                border: 1px solid #303030;  /* Same as section background */
            }
        """)

        tab_widget.addTab(table_view, 'Table')

    def setup_knockout_tab(self, tab_widget):
        ranked_teams = sorted(teams, key=lambda x: (x.points, x.NRR), reverse=True)

        # QGraphicsView widget for displaying tournament bracket
        knockout_tree = QGraphicsView()
        # QGraphicsScene to hold and manage the graphical elements of the bracket
        scene = QGraphicsScene(knockout_tree)
        # Set the created QGraphicsScene as the scene for the QGraphicsView
        knockout_tree.setScene(scene)

        # Create a QGraphicsRectItem representing a rectangle for semi-final
        # (X, Y, width, height)
        semifinal1_rect = QGraphicsRectItem(10, 10, 400, 200)
        scene.addItem(semifinal1_rect)  # Add the created rectangle item to the QGraphicsScene

        semifinal2_rect = QGraphicsRectItem(10, 300, 400, 200)
        scene.addItem(semifinal2_rect)

        final_rect = QGraphicsRectItem(550, 150, 400, 200)
        scene.addItem(final_rect)

        semifinal1_midpoint = semifinal1_rect.rect().center() + QPointF(200, 0)

        semifinal2_midpoint = semifinal2_rect.rect().center() + QPointF(200, 0)

        lineseg1 = QGraphicsLineItem(semifinal1_midpoint.x(), semifinal1_midpoint.y(), semifinal1_midpoint.x() + 70,
                                     semifinal1_midpoint.y())
        lineseg2 = QGraphicsLineItem(semifinal1_midpoint.x() + 70, semifinal1_midpoint.y(),
                                     semifinal1_midpoint.x() + 70, semifinal1_midpoint.y() + 90)
        lineseg3 = QGraphicsLineItem(semifinal1_midpoint.x() + 70, semifinal1_midpoint.y() + 90,
                                     semifinal1_midpoint.x() + 140, semifinal1_midpoint.y() + 90)

        lineseg4 = QGraphicsLineItem(semifinal2_midpoint.x(), semifinal2_midpoint.y(), semifinal2_midpoint.x() + 70,
                                     semifinal2_midpoint.y())
        lineseg5 = QGraphicsLineItem(semifinal2_midpoint.x() + 70, semifinal2_midpoint.y(),
                                     semifinal2_midpoint.x() + 70, semifinal2_midpoint.y() - 110)
        lineseg6 = QGraphicsLineItem(semifinal2_midpoint.x() + 70, semifinal2_midpoint.y() - 110,
                                     semifinal2_midpoint.x() + 140, semifinal2_midpoint.y() - 110)

        scene.addItem(lineseg1)
        scene.addItem(lineseg2)
        scene.addItem(lineseg3)
        scene.addItem(lineseg4)
        scene.addItem(lineseg5)
        scene.addItem(lineseg6)

        team1_sf1 = ranked_teams[0]
        team2_sf2 = ranked_teams[1]
        team3_sf2 = ranked_teams[2]
        team4_sf1 = ranked_teams[3]

        winner_sf1, runs1_sf1, wickets1_sf1, overs1_sf1, runs2_sf1, wickets2_sf1, overs2_sf1 = finals(
            team1_sf1, team4_sf1, 'Semi-Final 1')

        winner_sf2, runs1_sf2, wickets1_sf2, overs1_sf2, runs2_sf2, wickets2_sf2, overs2_sf2 = finals(
            team2_sf2, team3_sf2, 'Semi-Final 2')

        self.add_team_box(scene, team1_sf1, 10, 10, winner_sf1, runs1_sf1,
                          wickets1_sf1, overs1_sf1)
        self.add_team_box(scene, team4_sf1, 10, 110, winner_sf1, runs2_sf1,
                          wickets2_sf1, overs2_sf1)
        self.add_team_box(scene, team2_sf2, 10, 300, winner_sf2, runs1_sf2,
                          wickets1_sf2, overs1_sf2)
        self.add_team_box(scene, team3_sf2, 10, 400, winner_sf2, runs2_sf2,
                          wickets2_sf2, overs2_sf2)

        winner_final, runs1_final, wickets1_final, overs1_final, runs2_final, wickets2_final, overs2_final = finals(
            winner_sf1, winner_sf2, 'Final')

        self.add_team_box(scene, winner_sf1, 550, 150, winner_final, runs1_final, wickets1_final, overs1_final)
        self.add_team_box(scene, winner_sf2, 550, 250, winner_final, runs2_final, wickets2_final, overs2_final)

        winner_window = QGraphicsRectItem(550, 420, 400, 100)
        winner_flag_item = QGraphicsPixmapItem(get_team_flag(winner_final))
        winner_flag_item.setPos(620, 450)

        winner_team = QGraphicsTextItem(f"{winner_final.name}")
        winner_team.setFont(QFont("Arial", 16, QFont.Bold))  # Larger and bold font
        winner_team.setDefaultTextColor(QColor("#FFFFFF"))  # White color
        winner_team.setPos(650, 440)

        # Use QBrush for the background color
        background_brush = QBrush(QColor("#D4B911"))  # Modern blue color
        winner_window.setBrush(background_brush)

        # Use QPen for the border (set to NoPen for no border)
        border_pen = QPen(Qt.NoPen)
        winner_window.setPen(border_pen)

        trophy_path = "data/trophies/trophy1.jpg"
        trophy_pixmap = QPixmap(trophy_path).scaledToWidth(50)
        trophy_item = QGraphicsPixmapItem(trophy_pixmap)
        trophy_item.setPos(560, 435)

        winner_text = QGraphicsTextItem("WORLD CUP WINNERS")
        winner_text.setFont(QFont("Arial", 12, QFont.Bold))  # Larger and bold font
        winner_text.setDefaultTextColor(QColor("#FFFFFF"))  # White color
        winner_text.setPos(570, 380)

        # Apply shadow effect to the winner window
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setColor(QColor("#000000"))  # Black color for shadow
        shadow_effect.setOffset(0, 0)
        shadow_effect.setBlurRadius(10)
        winner_window.setGraphicsEffect(shadow_effect)

        scene.addItem(winner_window)
        scene.addItem(winner_flag_item)
        scene.addItem(winner_text)
        scene.addItem(winner_team)
        scene.addItem(trophy_item)

        scene.setBackgroundBrush(QBrush(QColor("#222222")))  # Matte black color

        # Set background color for rectangles
        semifinal1_rect.setBrush(QColor("#333333"))  # Darker matte black
        semifinal2_rect.setBrush(QColor("#333333"))
        final_rect.setBrush(QColor("#333333"))

        # Set line colors
        lineseg1.setPen(QPen(QColor("#FFFFFF")))  # White color for lines
        lineseg2.setPen(QPen(QColor("#FFFFFF")))
        lineseg3.setPen(QPen(QColor("#FFFFFF")))
        lineseg4.setPen(QPen(QColor("#FFFFFF")))
        lineseg5.setPen(QPen(QColor("#FFFFFF")))
        lineseg6.setPen(QPen(QColor("#FFFFFF")))

        tab_widget.addTab(knockout_tree, 'Knockout Tree')

    def add_team_box(self, scene, team, x, y, winner=None, runs=None, wickets=None, overs=None):
        box_width = 200
        box_height = 100

        # Team Box
        team_box = QGraphicsRectItem(x, y, box_width, box_height)
        team_box.setRect(0, 0, box_width, box_height)
        team_box.setPos(x, y)

        # Stylish gradient background
        gradient = QLinearGradient(0, 0, 0, 100)
        gradient.setColorAt(0, QColor("#013864"))        #3F13D4
        gradient.setColorAt(1, QColor("#5E6C6F"))       #2F97DA
        team_box.setBrush(gradient)

        # Rounded corners and shadow effect
        team_box.setPen(QPen(Qt.NoPen))

        team_box.setFlag(QGraphicsItem.ItemIsSelectable)
        team_box.setFlag(QGraphicsItem.ItemIsMovable)
        team_box.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3))

        # Result Box
        result_box = QGraphicsRectItem(x, y, box_width, box_height)
        result_box.setRect(0, 0, box_width, box_height)
        result_box.setPos(x + box_width, y)
        result_text = QGraphicsTextItem(f"{runs}/{wickets} in {overs} Overs")
        result_text.setFont(QFont("Ariel", 10))
        result_text.setPos(x + 210, y + 30)

        # Set result box style based on winner
        if winner == team:
            result_box.setBrush(QColor("#0FA23B"))  # Winner background color
        elif winner != team:
            result_box.setBrush(QColor("#A23535"))  # Loser background color with transparency

        # Flag Item
        flag_item = QGraphicsPixmapItem(get_team_flag(team))
        flag_item.setPos(x + 10, y + 40)

        # Team Name Item
        team_name_item = QGraphicsTextItem(team.name)
        team_name_item.setPos(x + 40, y + 30)
        team_name_item.setFont(QFont("Ariel"))

        # Set text color
        team_name_item.setDefaultTextColor(QColor("#ECF0F1"))  # White text color

        # Add items to the scene
        scene.addItem(team_box)
        scene.addItem(flag_item)
        scene.addItem(team_name_item)
        scene.addItem(result_box)
        scene.addItem(result_text)

    def setup_player_stats_tab(self, tab_widget):

        top5_runs, top5_wickets, top5_economy, top5_50s, top5_100s, top5_bat_avg = player_stats()

        positions = [(0, 0), (0, 1), (0, 2), (1,0), (1,1), (1,2)]

        player_stats_tab = QWidget()
        player_stats_layout = QGridLayout(player_stats_tab)

        for i, (title, data, type_attr, header_label, x, y) in enumerate(
            [
                ("Most Runs", top5_runs, 'runs', 'Runs', 10, 10),
                ("Most Wickets", top5_wickets, 'wickets_taken', 'Wickets', 10, 10),
                ('Most 50s', top5_50s, 'half_centuries', '50s', 10, 10),
                ('Most 100s', top5_100s, 'centuries', '100s', 10, 10),
                ('Best Economy', top5_economy, 'calc_economy', 'Economy', 10, 10),
                ('Best Batting Avg', top5_bat_avg, 'calc_bat_avg', 'Batting Average', 10, 10)
            ]
        ):
            table_widget = self.player_stats_table(title, data, type_attr, header_label, x, y)
            row, column = positions[i]
            player_stats_layout.addWidget(table_widget, row, column)

        player_stats_tab.setStyleSheet("background-color: #222222;")

        tab_widget.addTab(player_stats_tab, "Player Stats")

    def player_stats_table(self, title, player_list, type_attribute, header_label, x, y):
        try:
            table = QTableWidget()
            table.setMaximumSize(350, 400)
            table.setColumnCount(2)
            column_width = 200
            for column in range(2):
                table.setColumnWidth(column, column_width)
            table.setHorizontalHeaderLabels(['Player', header_label])
            table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
            table.setRowCount(5)
            row_height = 130
            for row in range(5):
                table.setRowHeight(row, row_height)

            for row, player in enumerate(player_list):
                player_path = f"data/Players/{player.name}.jpg"
                player_pixmap = QPixmap(player_path).scaledToWidth(50)

                player_widget = QWidget()
                player_layout = QVBoxLayout(player_widget)

                player_image_label = QLabel()
                player_image_label.setPixmap(player_pixmap)
                player_image_label.setStyleSheet(
                     "border: none;")
                player_layout.addWidget(player_image_label)

                name_label = QLabel(player.name)
                name_label.setStyleSheet("font-size: 16px; color: white; border: none;")
                matches_played_label = QLabel(f"<i>Matches Played: {player.matches_played}</i>")
                matches_played_label.setAlignment(Qt.AlignCenter)
                matches_played_label.setStyleSheet("font-size: 10px; color: white; border: none;")

                player_layout.addWidget(name_label)
                player_layout.addWidget(matches_played_label)

                table.setCellWidget(row, 0, player_widget)

                if callable(getattr(player, type_attribute, None)):
                    stat_value = getattr(player, type_attribute)()
                else:
                    # If not callable, treat it as an attribute
                    stat_value = getattr(player, type_attribute)

                if float(stat_value).is_integer():
                    formatted_value = str(stat_value)  # No decimal part, use as is

                else:
                    formatted_value = "{:.2f}".format(stat_value)  # Decimal part present, format with two decimal places

                stat_item = QTableWidgetItem(str(formatted_value))
                stat_item.setForeground(QBrush(Qt.white))

                table.setItem(row, 1, stat_item)


                if row == 0:
                    player_widget.setStyleSheet("border: 2px solid #FFD700;")  # Golden border for the first player


            table_height = sum(table.rowHeight(row) for row in range(table.rowCount()))
            table.setMaximumHeight(table_height + 35)

            table_width = sum(table.columnWidth(column) for column in range(table.columnCount()))
            table.setMaximumWidth(table_width + 40)

            title_label = QLabel(title)

            # Styling
            title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #FFFFFF;")  # Blue color for the title
            table.setStyleSheet("""
                QTableWidget {
                    background-color: #303030; /* Set background color */
                    border: 1px solid #bdc3c7; /* Set border color for a 3D effect */
                }
    
                QTableWidget::item {
                    color: white; /* Set font color to white */
                    padding: 2px;
                    border-bottom: 1px solid #cccccc; /* Set border color between rows */
                }
    
                QTableWidget::item:selected {
                    background-color: #a6e7ff; /* Set selected item background color */
                }
    
                QHeaderView::section {
                    background-color: #000000; /* Set header background color to black */
                    color: #ffffff; /* Set header text color to white */
                    padding: 3px;
                    border: 1px solid #2980b9; /* Set header border color */
                    font-size: 14px; /* Set font size for headers */
                    font-weight: bold;
                }
    
                QLabel {
                    font-size: 16px; /* Set font size for labels */
                    color: white; /* Set font color to white */
                }
            """)

            # Add 3D shading
            container_widget = QWidget()
            container_layout = QVBoxLayout(container_widget)
            container_layout.addWidget(title_label)
            container_layout.addWidget(table)

            # Add 3D effect to the container
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setColor(QColor(63, 63, 63, 180))  # Dark shadow color
            container_widget.setGraphicsEffect(shadow)

            return container_widget
        except Exception as e:
            print(f'error in player stats {e}')

    def setup_matches_tab(self, tab_widget):
        matches_scene = QGraphicsScene(self)

        box_width = 340
        box_height = 150
        margin_x = 35
        margin_y = 70
        num_columns = 5

        for i in range(1, 49):
            if i <= 45:
                id = f'Match#{i}'
            elif i == 46:
                id = f'Semi-Final 1'
            elif i == 47:
                id = f'Semi-Final 2'
            elif i == 48:
                id = f'Final'

            match = WorldCup.get_match(id)['match']
            row_index = (i - 1) // num_columns
            col_index = (i - 1) % num_columns
            x = col_index * (box_width + margin_x)
            y = row_index * (box_height + margin_y)

            box = SummaryBox(match, id, x, y, i ,matches_scene)
            box.setPos(x, y)
            matches_scene.addItem(box)

        matches_tab_content = QWidget()
        matches_layout = QGridLayout(matches_tab_content)

        clickable_boxes_view = QGraphicsView(matches_scene)
        clickable_boxes_view.setSceneRect(matches_scene.itemsBoundingRect())  # Adjust the scene rect

        matches_layout.addWidget(clickable_boxes_view, 0, 0)

        # Set the layout for the "Matches" tab
        matches_tab_content.setLayout(matches_layout)

        matches_tab_content.setStyleSheet("background-color: #303030;")  # Adjust the color code

        # Add the "Matches" tab to the main tab_widget
        tab_widget.addTab(matches_tab_content, 'Matches')


class SummaryBox(QGraphicsRectItem):
    blank_screen = None
    def __init__(self, match, match_id, x, y, i, scene=None):
        super(SummaryBox, self).__init__()

        self.match = match

        self.setRect(10, 10, 300, 150)
        self.innings1 = match.innings1
        self.innings2 = match.innings2

        team1 = self.innings1.batting_team
        team2 = self.innings2.batting_team

        text1 = f"{team1.name} {self.innings1.runs}/{self.innings1.wickets} in {self.innings1.overs} Overs"
        text2 = f"{team2.name} {self.innings2.runs}/{self.innings2.wickets} in {self.innings2.overs} Overs"
        text3 = f" {match.margin_of_victory}"
        if i <= 45:
            text4 = f"Group Stage: {match_id}"
        else:
            text4 = f'{match_id}'

        # Styling the text items
        font = QFont("Arial", 8, QFont.Bold)
        text_item1 = QGraphicsTextItem(text1, self)
        text_item2 = QGraphicsTextItem(text2, self)
        text_item3 = QGraphicsTextItem(text3, self)
        text_item4 = QGraphicsTextItem(text4, self)

        text_item1.setZValue(1)
        text_item2.setZValue(1)
        text_item3.setZValue(1)
        text_item4.setZValue(1)

        text_item1.setFont(font)
        text_item2.setFont(font)
        text_item3.setFont(font)
        text_item4.setFont(font)
        text_item1.setDefaultTextColor(Qt.white)  # White text color
        text_item2.setDefaultTextColor(Qt.white)
        text_item3.setDefaultTextColor(QColor("#E74C3C"))  # Red color for margin_of_victory
        text_item4.setDefaultTextColor(Qt.white)

        text_item1.setPos(x + 55, y + 60)
        text_item2.setPos(x + 55, y + 90)
        text_item3.setPos(x + 60, y + 130)
        text_item3.setTextWidth(300)
        text_item4.setPos(x + 10, y + 10)

        # Add team flags
        flag1 = QGraphicsPixmapItem(get_team_flag(team1))
        flag2 = QGraphicsPixmapItem(get_team_flag(team2))

        flag1.setPos(x + 20, y + 65)  # Adjust the position as needed
        flag2.setPos(x + 20, y + 95)

        flag1.setZValue(1)
        flag2.setZValue(1)

        # Add styling to the box
        self.setBrush(QBrush(QColor("#222222"), Qt.SolidPattern))  # Matte black background
        self.setPen(QPen(QColor("#222222"), 2))  # Border color matches background

        # Add drop shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(5, 5)
        self.setGraphicsEffect(shadow)

        if scene:
            scene.addItem(text_item1)
            scene.addItem(text_item2)
            scene.addItem(text_item3)
            scene.addItem(text_item4)
            scene.addItem(flag1)
            scene.addItem(flag2)


    def mousePressEvent(self, event):
        # Handle the click event here
        print("Clicked on SummaryBox")

        # Open an empty blank screen (another window)
        if not SummaryBox.blank_screen or not SummaryBox.blank_screen.isVisible():
            SummaryBox.blank_screen = MatchReport(match=self.match)
            SummaryBox.blank_screen.show()


class MatchReport(QWidget):
    def __init__(self, match):
        super().__init__()
        # Set up the blank screen widget
        self.setWindowTitle("Match Report")
        self.setGeometry(100, 100, 800, 600)

        innings1 = match.innings1
        innings2 = match.innings2

        # Create a tab widget
        self.tab_widget = QTabWidget(self)

        # Create tabs and add them to the tab widget
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()
        tab4 = QWidget()

        tab2_layout = QVBoxLayout(tab2)
        tab3_layout = QVBoxLayout(tab3)


        self.tab_widget.addTab(tab1, 'Summary')
        self.tab_widget.addTab(tab2, 'Innings 1')
        self.tab_widget.addTab(tab3, 'Innings 2')
        self.tab_widget.addTab(tab4, 'Run Rate')
        self.setup_run_rate(tab4, innings1, innings2)



        subtab2_widget_innings1 = QTabWidget(tab2)
        subtab2_scorecard_innings1 = QWidget()
        subtab2_commentary_innings1 = QWidget()

        subtab3_widget_innings2 = QTabWidget(tab3)
        subtab3_scorecard_innings2 = QWidget()
        subtab3_commentary_innings2 = QWidget()

        # Add subtabs to the main tab
        subtab2_widget_innings1.addTab(subtab2_scorecard_innings1, 'Score Card')
        subtab2_widget_innings1.addTab(subtab2_commentary_innings1, 'Commentary')

        subtab3_widget_innings2.addTab(subtab3_scorecard_innings2, 'Score Card')
        subtab3_widget_innings2.addTab(subtab3_commentary_innings2, 'Commentary')

        # Add the subtab widget to the layout
        tab2_layout.addWidget(subtab2_widget_innings1)
        tab3_layout.addWidget(subtab3_widget_innings2)

        self.setup_Summary(tab1, match)
        tab1.setStyleSheet("background-color: #222222;")
        tab2.setStyleSheet("background-color: #303030;")
        tab3.setStyleSheet("background-color: #303030;")
        tab4.setStyleSheet("background-color: #303030;")

        # Add content to each main tab
        tab_layout = self.setup_batting_scorecard_tab(subtab2_scorecard_innings1,  innings1.batting_team_stats,
                                                      innings1.batting_team.name, innings1.fall_of_wickets)

        try:
            self.setup_bowling_scorecard(subtab2_scorecard_innings1, innings1.bowling_team_stats, innings1.bowling_team.name, tab_layout, innings1.extras)
        except Exception as e:
            print(f"Error in setup_bowling_scorecard: {e}")

        tab_layout2 = self.setup_batting_scorecard_tab(subtab3_scorecard_innings2,  innings2.batting_team_stats,
                                                       innings2.batting_team.name, innings2.fall_of_wickets)

        try:
            self.setup_bowling_scorecard(subtab3_scorecard_innings2, innings2.bowling_team_stats, innings2.bowling_team.name, tab_layout2, innings2.extras)
        except Exception as e:
            print(f"Error in setup_bowling_scorecard: {e}")

        try:
            self.setup_Commentary_tab(subtab2_commentary_innings1, innings1)
            self.setup_Commentary_tab(subtab3_commentary_innings2, innings2)
        except Exception as e:
            print(f"Error in Commentary tab: {e}")

        # Set up the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.tab_widget)
        self.setFixedSize(800, 920)

        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y-120)


        try:
            self.tab_widget.currentChanged.connect(self.updateWindowSize)
        except Exception as e:
            print(f"{e}!!")

    def updateWindowSize(self):
        index = self.tab_widget.currentIndex()
        current_tab_name = self.tab_widget.tabText(index)
        tab_sizes = {
            'Summary': (800, 920),
            'Innings 1': (900, 1080),
            'Innings 2': (900, 1080),
            'Run Rate' : (800, 920)
        }
        self.setFixedSize(*tab_sizes.get(current_tab_name))

    def setup_batting_scorecard_tab(self, tab, batting_stats, team_name, fow):
        table = QTableWidget(tab)
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(['Player', 'Runs', 'Balls', 'Strike Rate', 'Dismissal'])

        for player, stats in batting_stats.items():
            row_position = table.rowCount()
            table.insertRow(row_position)

            table.setItem(row_position, 0, QTableWidgetItem(player))

            # Check if balls played is zero
            if stats['balls_played'] > 0:
                table.setItem(row_position, 1, QTableWidgetItem(str(stats['runs_scored'])))
                table.setItem(row_position, 2, QTableWidgetItem(str(stats['balls_played'])))
                strike_rate = (stats['runs_scored'] / stats['balls_played']) * 100
                table.setItem(row_position, 3, QTableWidgetItem(f"{strike_rate:.2f}"))
                dismissal_type = stats['dismissal_type'] or "Not Out"
                dismissed_by = stats['dismissed_by'] or "N/A"
                if stats['dismissal_type'] == "Caught":
                    dismissal_type = f"{dismissal_type} by {stats['fielder'] or 'N/A'}"
                table.setItem(row_position, 4, QTableWidgetItem(f"{dismissal_type}, {dismissed_by}"))
            else:
                # Merge columns for "Did Not Bat"
                table.setSpan(row_position, 1, 1, 5)
                table.setItem(row_position, 1, QTableWidgetItem("Did Not Bat"))

        table.setVerticalHeaderLabels([str(i + 1) for i in range(table.rowCount())])

        # Adjust column widths to contents

        # Set the team name in the table header
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        table.setHorizontalHeaderLabels(['Player', 'Runs', 'Balls', 'Strike Rate', 'Dismissal'])

        total_width = 0
        total_height = 0
        for i in range(table.columnCount()):
            total_width += table.columnWidth(i)
        for i in range(table.rowCount()):
            total_height += table.rowHeight(i)

        table.setFixedSize(total_width, total_height)


        # Set the maximum width for the window
        tab.setMaximumWidth(900)
        table.resizeColumnsToContents()

        # Set up the layout
        tab_layout = QVBoxLayout(tab)

        team_name_label = QLabel(f'Batting Scorecard - {team_name}')
        team_name_label.setStyleSheet("color: #3498DB; font-size: 18px; font-weight: bold;")

        tab_layout.addWidget(team_name_label)
        tab_layout.addWidget(table)

        fow_line = ', '.join(str(wicket) for wicket in fow.values() if wicket != '')
        if fow_line:
            fow_label = QLabel(f'Fall of Wickets: {fow_line}')
            fow_label.setStyleSheet("color: #E74C3C; font-size: 14px;")
            tab_layout.addWidget(fow_label)

        tab.setLayout(tab_layout)

        # Apply style sheet
        table.setStyleSheet("""
            QTableWidget {
                background-color: #5D6D7E; /* Set background color */
                alternate-background-color: #e0e0e0; /* Set alternate row background color */
                border: 2px solid #95a5a6; /* Set border color for a 3D effect */
            }

            QTableWidget::item {
                color: #ffffff; /* Set font color to white */
                padding: 8px;
                border-bottom: 1px solid #cccccc; /* Set border color between rows */
            }

            QTableWidget::item:selected {
                background-color: #a6e7ff; /* Set selected item background color */
            }

            QHeaderView::section {
                background-color: #222222; /* Set header background color */
                color: #ffffff; /* Set header text color */
                padding: 8px;
                border: 1px solid #2980b9; /* Set header border color */
                font-size: 14px; /* Set font size for headers */
                font-weight: bold;
            }

            QLabel {
                font-size: 18px; /* Set font size for labels */
                margin-bottom: 10px;
                color: #ffffff; /* Set font color to white */
            }
        """)

        return tab_layout

    def setup_bowling_scorecard(self, tab, bowling_stats, team_name, layout, extras):
        try:
            # Create the table
            table = QTableWidget(tab)
            table.setColumnCount(5)

            # Set table styles
            table.setStyleSheet("""
                QTableWidget {
                    background-color: #5D6D7E; /* Set background color */
                    alternate-background-color: #e0e0e0; /* Set alternate row background color */
                    border: 2px solid #95a5a6; /* Set border color for a 3D effect */
                }

                QTableWidget::item {
                    color: #ffffff; /* Set font color to white */
                    padding: 8px;
                    border-bottom: 1px solid #cccccc; /* Set border color between rows */
                }

                QTableWidget::item:selected {
                    background-color: #a6e7ff; /* Set selected item background color */
                }

                QTableWidget::item[padding="numbers"] {
                    padding-left: 20px; /* Add left padding for numbers */
                }
            """)

            table.setHorizontalHeaderLabels(['Bowler', 'O', 'W', 'R', 'Economy'])

            # Explicitly style the header
            header = table.horizontalHeader()
            header.setStyleSheet("""
                QHeaderView::section {
                    background-color: #000000; /* Set header background color to black */
                    color: #ffffff; /* Set header text color to white */
                    padding: 8px;
                    border: 1px solid #2980b9; /* Set header border color */
                    font-size: 14px; /* Set font size for headers */
                    font-weight: bold;
                }
            """)

            # Populate the table with bowling stats
            for player, stats in bowling_stats.items():
                if stats['overs_bowled'] > 0:
                    row_position = table.rowCount()
                    table.insertRow(row_position)

                    table.setItem(row_position, 0, QTableWidgetItem(player))
                    table.setItem(row_position, 1, QTableWidgetItem(str(stats['overs_bowled'])))
                    table.setItem(row_position, 2, QTableWidgetItem(str(stats['wickets'])))
                    table.setItem(row_position, 3, QTableWidgetItem(str(stats['runs_conceded'])))

                    economy = stats['runs_conceded'] / stats['overs_bowled']
                    table.setItem(row_position, 4, QTableWidgetItem(f'{economy:.2f}'))

            # Adjust column sizes and set team name
            table.resizeColumnsToContents()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

            # Set the team name in the table header
            team_name_label = QLabel(f'Bowling Scorecard - {team_name}')
            team_name_label.setStyleSheet("color: #3498DB; font-size: 18px; font-weight: bold;")

            total_height = 0
            total_width = 0
            for i in range(table.rowCount()):
                total_height += table.rowHeight(i)
            for i in range(table.columnCount()):
                total_width += table.columnWidth(i)

            # Display the team name and table
            layout.addWidget(team_name_label)
            layout.addWidget(table)
            table.setFixedSize(total_width+50, total_height+50)

            # Display Extras under Bowling Scorecard
            extras_label = QLabel(
                f'Extras: {extras["No Ball"] + extras["Wide"]} (Nb: {extras["No Ball"]}, Wd: {extras["Wide"]})')
            extras_label.setStyleSheet("color: #E74C3C; font-size: 14px;")
            layout.addWidget(extras_label)

            # Set the layout for the tab
            tab.setLayout(layout)

        except Exception as e:
            print(f"Error in setup_bowling_scorecard: {e}")

    def setup_Summary(self, tab, match):
        try:

            innings1 = match.innings1
            innings2 = match.innings2

            innings1_batting = innings1.batting_team_stats
            innings1_bowling = innings1.bowling_team_stats

            innings2_batting = innings2.batting_team_stats
            innings2_bowling = innings2.bowling_team_stats

            # Innings 1
            scene = QGraphicsScene(tab)
            view = QGraphicsView(scene)

            x = -320

            flag_item1 = QGraphicsPixmapItem(QPixmap(get_team_flag(innings1.batting_team).scaledToWidth(60)))
            flag_height1 = flag_item1.pixmap().height()
            flag_item1.setPos(x, -630)

            name_item1 = QGraphicsTextItem(f"{innings1.batting_team.name}")
            name_item1.setFont(QFont("Arial", 10))
            name_item1.setDefaultTextColor(Qt.white)
            name_x = flag_item1.pos().x() + (flag_item1.pixmap().width() - name_item1.boundingRect().width()) / 2
            name_item1.setPos(name_x, -580)

            # Center the score to the right of the flag
            score_item1 = QGraphicsTextItem(f"{innings1.runs}/{innings1.wickets} ({innings1.overs})")
            score_item1.setDefaultTextColor(Qt.white)
            score_item1.setFont(QFont('Ariel', 8))
            score_item1.setPos(flag_item1.pos().x() + 75,
                               flag_item1.pos().y() + (flag_height1 - score_item1.boundingRect().height()) / 2)

            flag_item2 = QGraphicsPixmapItem(QPixmap(get_team_flag(innings2.batting_team).scaledToWidth(60)))
            flag_width2 = flag_item2.pixmap().width()
            flag_height2 = flag_item2.pixmap().height()
            flag_item2.setPos(x + 350, -630)

            name_item2 = QGraphicsTextItem(f"{innings2.batting_team.name}")
            name_item2.setFont(QFont("Arial", 10))
            name_item2.setDefaultTextColor(Qt.white)
            name2_x = flag_item2.pos().x() + (flag_width2 - name_item2.boundingRect().width()) / 2
            name_item2.setPos(name2_x, -580)

            # Center the score to the left of the flag
            score_item2 = QGraphicsTextItem(f"{innings2.runs}/{innings2.wickets} ({innings2.overs})")
            score_item2.setDefaultTextColor(Qt.white)
            score_item2.setFont(QFont('Ariel', 8))
            score_item2.setPos(flag_item2.pos().x() - 105,
                               flag_item1.pos().y() + (flag_height2 - score_item2.boundingRect().height()) / 2)

            # Align the result_item between the last letter of the left name and the first letter of the right name
            result_item = QGraphicsTextItem(f"{match.margin_of_victory}")
            result_item.setDefaultTextColor(Qt.white)
            result_item.setFont(QFont('Ariel', 8))
            result_x = name_item1.pos().x() + name_item1.boundingRect().width() + (name_item2.pos().x() - (
                    name_item1.pos().x() + name_item1.boundingRect().width())) / 2 - result_item.boundingRect().width() / 2
            result_item.setPos(result_x, -580)

            toss_item = QGraphicsTextItem(
                f"TOSS: {match.toss_winner.name} won the toss and decided to {match.toss_decision}")
            toss_item.setPos(-450, -30)
            toss_item.setFont(QFont('Ariel', 9))
            toss_item.setDefaultTextColor(Qt.white)

            stadium_item = QGraphicsTextItem(f"STADIUM: {match.stadium.name}")
            stadium_item.setPos(-450, 0)
            stadium_item.setFont(QFont('Ariel', 9))
            stadium_item.setDefaultTextColor(Qt.white)

            pitch_item = QGraphicsTextItem(f"PITCH: {match.stadium.pitch_type.pitch_type.value}")
            pitch_item.setPos(-450, 30)
            pitch_item.setFont(QFont('Ariel', 9))
            pitch_item.setDefaultTextColor(Qt.white)

            match_num_item = QGraphicsTextItem(f"{WorldCup.get_match_id_by_object(match)}")
            match_num_x = name_item1.pos().x() + name_item1.boundingRect().width() + (name_item2.pos().x() - (
                    name_item1.pos().x() + name_item1.boundingRect().width())) / 2 - match_num_item.boundingRect().width() / 2

            match_num_item.setPos(match_num_x, -550)
            match_num_item.setFont(QFont('Ariel', 9))
            match_num_item.setDefaultTextColor(Qt.white)

            def draw_head_and_lines(scene, team, runs, wickets, overs, x, y):
                head = QGraphicsTextItem(f"{team.name} {runs}/{wickets} ({overs})")
                head.setPos(x, y)
                head.setDefaultTextColor(Qt.white)
                head.setFont(QFont('Ariel', 8))


                flag = QGraphicsPixmapItem(get_team_flag(team))
                flag.setPos(x - 35, y + 5)

                left_line = QGraphicsLineItem(-900, y + (head.boundingRect().height() / 2),
                                              flag.pos().x() - 10, y + (head.boundingRect().height() / 2))
                right_line = QGraphicsLineItem(x + head.boundingRect().width(),
                                               y + (head.boundingRect().height() / 2), 800,
                                               y + (head.boundingRect().height() / 2))

                # Set the color of the lines to white
                pen = QPen(QColor(Qt.white))
                left_line.setPen(pen)
                right_line.setPen(pen)

                scene.addItem(head)
                scene.addItem(flag)
                scene.addItem(left_line)
                scene.addItem(right_line)


            def draw_top_players(scene, top_players, x, y):
                for idx, (player_name, player_stats) in enumerate(top_players):

                    player_image_path = f"data/Players/{player_name}.jpg"  # Replace with actual image path

                    # Image
                    player_image = QGraphicsPixmapItem(QPixmap(player_image_path).scaledToWidth(40))
                    player_image.setPos(x-40, (y-10) + idx * 50)  # Adjust the y-coordinate based on your layout
                    scene.addItem(player_image)


                    if 'runs_scored' in player_stats:
                        player_runs = player_stats['runs_scored']
                        player_balls_played = player_stats['balls_played']
                        player_info = QGraphicsTextItem(f"{player_name}  {player_runs} ({player_balls_played})")
                    elif 'wickets' in player_stats:
                        player_wickets = player_stats['wickets']
                        player_runs_conceded = player_stats['runs_conceded']
                        player_overs_bowled = player_stats['overs_bowled']
                        player_info = QGraphicsTextItem(
                            f"{player_name}  {player_wickets}/{player_runs_conceded} ({player_overs_bowled})")

                    player_info.setPos(x, y + idx * 50)
                    player_info.setDefaultTextColor(Qt.white)
                    player_info.setFont(QFont('Ariel', 8))
                    scene.addItem(player_info)

            draw_head_and_lines(scene, innings1.batting_team, innings1.runs, innings1.wickets, innings1.overs, -200, -500)
            draw_top_players(scene,
                             sorted(innings1_batting.items(), key=lambda x: x[1]['runs_scored'], reverse=True)[:3],
                             -405, -450)
            draw_top_players(scene, sorted(innings1_bowling.items(), key=lambda x: x[1]['wickets'], reverse=True)[:3],
                             -15, -450)

            draw_head_and_lines(scene, innings2.batting_team, innings2.runs, innings2.wickets, innings2.overs, -200, -300)

            draw_top_players(scene,
                             sorted(innings2_batting.items(), key=lambda x: x[1]['runs_scored'], reverse=True)[:3],
                             -405, -250)
            draw_top_players(scene, sorted(innings2_bowling.items(), key=lambda x: x[1]['wickets'], reverse=True)[:3],
                             -15, -250)

            scene.addItem(flag_item1)
            scene.addItem(name_item1)
            scene.addItem(flag_item2)
            scene.addItem(name_item2)
            scene.addItem(score_item1)
            scene.addItem(score_item2)
            scene.addItem(result_item)
            scene.addItem(toss_item)
            scene.addItem(stadium_item)
            scene.addItem(pitch_item)
            scene.addItem(match_num_item)


            tab_layout = QVBoxLayout(tab)
            tab_layout.addWidget(view)
            tab.setLayout(tab_layout)

            scene.setSceneRect(-300, -600, 400, 600)

            view.setStyleSheet(
                """
                 QGraphicsView {
                background-color: #303030; /* Set background color */
            }
                """
            )

        except Exception as e:
            print(f"Error in setting up Summary: {e}")

    def setup_Commentary_tab(self, tab, innings):
        # Create a QTextBrowser for displaying commentary
        commentary_browser = QTextBrowser(tab)
        commentary_browser.setTextInteractionFlags(commentary_browser.textInteractionFlags() | Qt.LinksAccessibleByMouse)
        commentary_browser.setOpenExternalLinks(True)

        # Set up the layout
        layout = QVBoxLayout(tab)
        layout.addWidget(commentary_browser)

        # Initialize variables to track over summary
        total_runs, total_wickets, total_extras = 0, 0, 0

        # Iterate through each over in innings_data and display commentary
        for over_index, over_data in enumerate(innings.innings_data, start=1):
            commentary_browser.append(
                f"<span style='color:white; font-weight:bold;'>Over {over_index}:</span>"
            )

            for ball_index, ball_data in enumerate(over_data, start=1):
                bowler = ball_data['bowler']
                striking_batsman = ball_data['striking_batsman']
                ball_outcome = ball_data['outcome']

                # Determine the color based on ball_outcome value
                color = self.get_color_for_outcome(ball_outcome)

                # Append commentary to the QTextBrowser with color
                commentary_browser.append(
                    f"<span style='color:white;'>{over_index - 1}.{ball_index}: {bowler} to {striking_batsman} "
                    f"<span style='color:{color}'>{ball_outcome}</span></span>"
                )

            # Calculate over summary
            over_summary = self.calculate_over_summary(over_data)
            total_runs += over_summary['runs']
            total_wickets += over_summary['wickets']
            total_extras += over_summary['extras']

            # Append end of over summary
            commentary_browser.append(
                f"<br/><span style='color:white;'>"
                f"<b>End of Over</b> {over_index}: "
                f"Runs: {over_summary['runs']}, Wickets: {over_summary['wickets']}, Extras: {over_summary['extras']}<br/></span>"
            )

        # Set the layout for the tab
        tab.setLayout(layout)

    def get_color_for_outcome(self, ball_outcome):
        # Assign colors based on ball_outcome value
        if ball_outcome in [0, 1, 2, 3, 4, 6]:
            return '#0EE100'  # Color for runs
        elif ball_outcome in ['Bowled', 'Caught', 'LBW', 'Direct Hit', 'Missed', 'Dropped', 'Stumped']:
            return '#FF2200'  # Color for dismissals
        elif ball_outcome in ['Wide', 'No Ball']:
            return '#00FFF9'  # Color for extras
        else:
            return 'white'  # Default color

    def calculate_over_summary(self, over_data):
        # Initialize summary variables
        runs, wickets, extras = 0, 0, 0

        # Iterate through each ball in the over_data
        for ball_data in over_data:
            ball_outcome = ball_data['outcome']

            if ball_outcome in [0, 1, 2, 3, 4, 6]:
                runs += ball_outcome
            elif ball_outcome in ['Bowled', 'LBW', 'Stumped', 'Caught', 'Direct Hit']:
                wickets += 1
            elif ball_outcome in ['Wide', 'No Ball']:
                extras += 1

        return {'runs': runs, 'wickets': wickets, 'extras': extras}

    def setup_run_rate(self, tab, innings1, innings2):
        try:
            run_rate1 = innings1.run_rate
            run_rate2 = innings2.run_rate

            overs1 = [0] + list(run_rate1.keys())  # Ensure the first point is at (0, 0)
            total_runs1 = [0] + [data['total_runs'] for data in run_rate1.values()]
            wickets1 = [data['team_wickets'] for data in run_rate1.values()]

            overs2 = [0] + list(run_rate2.keys())  # Ensure the first point is at (0, 0)
            total_runs2 = [0] + [data['total_runs'] for data in run_rate2.values()]
            wickets2 = [data['team_wickets'] for data in run_rate2.values()]

            # Create a figure and axis
            fig, ax = plt.subplots()

            # Plot the run rate data
            line1, = ax.plot(overs1, total_runs1, linestyle='-', color='b', label=f'{innings1.batting_team.name}')
            line2, = ax.plot(overs2, total_runs2, linestyle='-', color='g', label=f'{innings2.batting_team.name}')

            initial_wickets1 = 0
            # Add markers for wicket falls in innings1
            for over, wicket in zip(overs1, wickets1):
                if wickets1[overs1.index(over)] - initial_wickets1 == 1:
                    ax.plot(over, total_runs1[overs1.index(over)], marker='x', markersize=8, color='red')
                    initial_wickets1 = wickets1[overs1.index(over)]
                elif wickets1[overs1.index(over)] - initial_wickets1 > 1:
                    for i in range(wickets1[overs1.index(over)] - initial_wickets1):
                        ax.plot(over, total_runs1[overs1.index(over)], marker='x', markersize=8+5*i, color='#FB7171')
                        initial_wickets1 = wickets1[overs1.index(over)]

            initial_wickets2 = 0
            # Add markers for wicket falls in innings2
            for over, wicket in zip(overs2, wickets2):
                if wickets2[overs2.index(over)] - initial_wickets2 == 1:
                    ax.plot(over, total_runs2[overs2.index(over)], marker='x', markersize=8, color='yellow')
                    initial_wickets2 = wickets2[overs2.index(over)]
                elif wickets2[overs2.index(over)] - initial_wickets2 > 1:
                    for i in range(wickets2[overs2.index(over)] - initial_wickets2):
                       ax.plot(over, total_runs2[overs2.index(over)], marker='x', markersize=8+5*i, color='#F4F99E')
                       initial_wickets2 = wickets2[overs2.index(over)]

            # Set the font color to white
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')

            # Set the background color to black
            ax.set_facecolor('#222222')
            ax.figure.set_facecolor('#303030')

            # Create separate legends for each innings
            legend1 = ax.legend(
                [Line2D([0], [0], color='b', lw=2), Line2D([0], [0], color='red', marker='x', markersize=8)],
                [f'{innings1.batting_team.name}', 'Wicket'],
                facecolor='black', edgecolor='white', labelcolor='white'
                # Set the legend background color, edge color, and label color
            )

            legend2 = ax.legend(
                [Line2D([0], [0], color='g', lw=2), Line2D([0], [0], color='yellow', marker='x', markersize=8)],
                [f'{innings2.batting_team.name}', 'Wicket'],
                loc='center left',
                facecolor='black', edgecolor='white', labelcolor='white'
                # Set the legend background color, edge color, and label color
            )

            # Combine legends
            ax.add_artist(legend1)
            ax.add_artist(legend2)

            ax.text(0.5, 1.05, 'Run Rate', transform=ax.transAxes, color='white', fontsize=14, ha='center', va='center')
            ax.grid(True, linestyle='--', alpha=0.7, color='white')

            # Add the plot to the tab
            layout = QVBoxLayout(tab)
            layout.addWidget(FigureCanvasQTAgg(fig))

        except Exception as e:
            print(f"Error in setup_run_rate: {e}")


try:
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = IntroScreen(CricketWorldCup())
        window.show()
        sys.exit(app.exec_())
except Exception as e:
    print(f"{e}")
