# -*- coding: utf-8 -*-
"""
/***************************************************************************
 wtyczka
                                 A QGIS plugin
 wtyczka aaaaaa
                              -------------------
        begin                : 2015-01-17
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Paulina
        email                : dc@fs.pl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from wtyczka_a_dialog import wtyczkaDialog
import os.path
import json, urllib
import time, calendar
from qgis.core import *
from qgis.gui import *


class wtyczka:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'wtyczka_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = wtyczkaDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&wtyczka')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'wtyczka')
        self.toolbar.setObjectName(u'wtyczka')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('wtyczka', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/wtyczka/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'wtyczka'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&wtyczka'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
		
		#Paulina Sosnowska
		#GiK I MSU
		#grupa 4 
		
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
			
			#podłączenie pliku shp z województwami
			woj=os.path.join("c:/Users/Paula/.qgis2/python/plugins/wtyczka/shp/admin_region_teryt_woj.shp")
			#nowa warstwa wektorowa (ogr-biblioteka do formatów rastrowych)
			woj_warstwa=QgsVectorLayer(woj,"Wojewodztwa","ogr")
			# aktualizacja zasięgu i dodanie warstwy do wyświetlenia 
			QgsMapLayerRegistry.instance().addMapLayer(woj_warstwa)
			
			#rozpoczynam edycję wartwy
			woj_warstwa.startEditing()
			
			#dodawanie kolumn
			columns=["TEMP","TEMP_MAX","TEMP_MIN", "CISNIENIE","WILGOTNOSC","V_WIATRU","K_WIATRU","CHMURY"]
			
			for i in columns:
			#zwraca obiekt reprezentujący moduł odpowiedzialny za obsługę danej warstwy wektorowej 
				if woj_warstwa.dataProvider().fieldNameIndex(i)==-1:
					woj_warstwa.dataProvider().addAttributes([QgsField('Miasto', QVariant.String), QgsField('Temp', QVariant.Int), QgsField('TempMin', QVariant.Int), QgsField('TempMax', QVariant.Int), QgsField('Cisnienie', QVariant.Double), QgsField('Wilgotnosc', QVariant.Double), QgsField('PredkWiatru', QVariant.Double), QgsField('KierWiatru', QVariant.Double), QgsField('Chmury', QVariant.Int)])
			woj_warstwa.updateFields()
			#dane - ścieżka z plikami geojeson
			dane=os.path.join("c:/Users/Paula/.qgis2/python/plugins/wtyczka/wojewo.json")
			#pobranie danych dla  miast wojewódzkich
			link="http://api.openweathermap.org/data/2.5/group?units=metric&id=858791,3337496,3337499,3337500,858789,858785,858787,3337494,3337493,3337498,858790,3337492,3337495,3337497,858788,858786"
			# warsaw # zg # szczecin # gdansk # olsztyn # bialystok # lublin # rzeszow # katowice # krakow # opole # wroclaw # poznan # bydgoszcz # kielce # lodz#
				
			t_teraz=calendar.timegm(time.gmtime())
			
			try:
				plik=open(dane,'r')
			except IOError:
				plik=open(dane,'w+')
			plikdane=plik.read()
			plik.close()
			
			try:
				dane3=json.loads(plikdane)
				if 'data' in dane3:
					t_dane=dane3['data']
				else:
					t_dane=0
			except ValueError:
				t_dane=0
						
			if t_teraz-t_dane>600:
				plik2=open(dane,'w+')
				odp=urllib.urlopen(link)
				dane2=json.loads(odp.read())
				odp.close()
				plik2.write(json.dumps(dane2,plik2))
				plik2.close()
			else:
				dane2=dane3
			
			#uaktualnianie danych o pogodzie
			woj_warstwa.startEditing()
			pogoda=dane2['list']
			wartosci2=[]
			ikonki=[]
			link_ikonki="http://openweathermap.org/img/w/"
			for i in range(0,len(pogoda)):
				temperatura=pogoda[i]['main']['temp']
				temperatura_max=pogoda[i]['main']['temp_max']
				temperatura_min=pogoda[i]['main']['temp_min']
				cisnienie=pogoda[i]['main']['pressure']
				wilgotnosc=pogoda[i]['main']['humidity']
				predkosc_wiatru=pogoda[i]['wind']['speed']
				kier_wiatru=pogoda[i]['wind']['deg']
				chmury=pogoda[i]['clouds']['all']
				wartosci=[temperatura, temperatura_max, temperatura_min, cisnienie, wilgotnosc, predkosc_wiatru, kier_wiatru,chmury]
				wartosci2.append(wartosci)
			it=-1
			for element in woj_warstwa.getFeatures():
				it=it+1
				for k in xrange(0, len(columns)):
						element.setAttribute(columns[k],wartosci2[it][k])
				woj_warstwa.updateFeature(element)
			woj_warstwa.commitChanges()
			QgsMapLayerRegistry.instance().addMapLayer(woj_warstwa)	
			woj_warstwa.updateExtents()

        pass
