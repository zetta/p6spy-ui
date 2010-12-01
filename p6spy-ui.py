#!/usr/bin/env python
import array
import csv
import sys
import pango 
try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	pass
try:
	import gtk
  	import gtk.glade
except:
	sys.exit(1)


class P6SpyMain:
	"""This is an Hello World GTK application"""

	def __init__(self):
	
		self.xml = gtk.glade.XML("view.glade")
		self.xml.signal_connect("fileChooser", self.on_open_button)
		self.window = self.xml.get_widget("mainWindow")
		self.chooser = None
		self.window.set_title("p6spy Graphic Viewer")
		self.reload = self.xml.get_widget("reloadButton")

		self.progress = self.xml.get_widget("mainProgressBar")
		self.reload.set_sensitive (False)
		self.combo = self.xml.get_widget("mainCombo")
		self.xml.signal_connect("fileReloader", self.on_reload_button)
		if (self.window):
			self.window.connect("destroy", gtk.main_quit)
		self.create_tags()

	def create_tags(self):
		self.text = self.xml.get_widget("mainText")		
		self.buffer = self.text.get_buffer()
		h_tag = self.buffer.create_tag( "h", size_points=16, weight=pango.WEIGHT_BOLD)
		i_tag = self.buffer.create_tag( "i", style=pango.STYLE_ITALIC) 
		c_tag = self.buffer.create_tag( "colored", foreground="#FFFF00", background="#0000FF") 
		e_tag = self.buffer.create_tag( "fixed", editable=False)
		d_tag = self.buffer.create_tag( "date", size_points=9, foreground="#666666" )
		t_tag = self.buffer.create_tag( "title", size_points=9, foreground="#0074DE" )
		t_tag = self.buffer.create_tag( "query", size_points=12, foreground="#222222" )
		t_tag = self.buffer.create_tag( "line", size_points=2, foreground="#CCCCCC", background="#CCCCCC" )

	def on_reload_button(self, evt):
		self.load_file(self.chooser.get_filename())	

	def on_open_button(self, evt):
		print "abriendo..."

		if(None!=self.chooser):
			self.chooser.destroy()
		self.chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_OPEN,
			buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))


		filter = gtk.FileFilter()
		filter.set_name("p6Spy Log Files")
		filter.add_pattern("*.log")
		self.chooser.add_filter(filter)
		self.chooser.set_default_response(gtk.RESPONSE_OK)
		self.chooser.set_title("Seleccione el archivo...")
		response = self.chooser.run()

		
		if response == gtk.RESPONSE_OK:
			self.load_file(self.chooser.get_filename())
			self.chooser.hide()
		elif response == gtk.RESPONSE_CANCEL:
			print 'Closed, no files selected'
			self.chooser.hide()
		self.reload.set_sensitive(True)

	def load_file(self, fileName):
		self.progress.show()
		self.fileContents = csv.reader(open(fileName, 'rb'), delimiter='|')
		
		
		position = self.buffer.get_end_iter()
		self.buffer.insert_with_tags_by_name( position, "Log\n", 'h')

		
		
		for row in self.fileContents:
			self.progress.pulse()

			position = self.buffer.get_end_iter()
			self.buffer.insert_with_tags_by_name( position, row[0]+"\n", 'date')
			position = self.buffer.get_end_iter()
			self.buffer.insert_with_tags_by_name( position, row[3]+"\n", 'title')
			
			query = row[4] and row[4] or row[5]
			position = self.buffer.get_end_iter()
			self.buffer.insert_with_tags_by_name( position, "\t"+query+"\n", 'query')

			position = self.buffer.get_end_iter()
			self.buffer.insert_with_tags_by_name( position, "-----------------------------------------------------------"+
				"---------------------------------------------------------------------------\n\n", 'line')
		
			


		self.progress.hide()
		#self.progress.set_activity_mode(False)
		#cell = gtk.CellRendererText()
		#self.combo.add_attribute(cell, 'text', 0)
		#self.combo.connect('changed', self.changed_cb) el disparador

		#self.combo.set_sensitive(False)

		
	 	# create a TreeStore with one string column to use as the model
		#self.treestore = gtk.TreeStore(str)
   
        # we'll add some data now - 4 rows with 3 child rows each
		#for row in self.fileContents:
		#	piter = self.treestore.append(None, ['parent %i' % row])
		#	for child in row:
		#		self.treestore.append(piter, ['child %i of parent %i' % (child, row)])

		#self.tree = self.xml.get_widget("mainTree")
		#self.tree

		#print (self.fileContents)
		#for row in self.fileContents:
		#	print ', '.join(row)
		#for line in self.fileContents:
		#	print ("una linea, ")




if __name__ == "__main__":
	app = P6SpyMain()
	gtk.main()






























