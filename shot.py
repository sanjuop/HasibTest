import os

import pymel.core as pm


class MayaShot(object):
	def __init__(self, shot_name=None, shot_path=None):
		if shot_name:
			shot_name = shot_name
		elif shot_path:
			shot_name = pm.Path(shot_path).basename()
		elif pm.sceneName():
			shot_name = pm.sceneName().basename()
		else:
			raise ValueError("Shot name is invalid")
		
		all_parts = shot_name.split(".")[0].split("_")
		
		if len(all_parts) < 4:
			raise ValueError("Shot name is invalid")
		
		self.project_code = all_parts[0]
		self.episode = all_parts[1]
		self.sequence = all_parts[2]
		self.shot = all_parts[3]
		self.shot_name = self.project_code+"_"+self.episode+"_"+self.sequence+"_"+self.shot
		
	def __repr__(self):
		return "Maya Shot {}".format(self.shot_name)
		
	def __str__(self):
		return self.shot_name
		
	def local_path(self):
		workspace_path = pm.internalVar(uwd=1)
		return workspace_path
		
	def get_playblast_dir(self):
		playblast_dir = os.path.join(self.local_path(), "default", "movies")
		return playblast_dir
		
	def get_playblast_path(self):
		scene_name = self.shot_name
		playblast_path = os.path.join(self.get_playblast_dir(), "default", "movies", scene_name)
		return playblast_path
		

	def get_scene_name(self, full_path=False, basename=False, dir_base=False):
		scene_name = pm.sceneName()
		if scene_name == "":
			pm.confirmDialog(m="File not open",b="Ok")
			return
		elif full_path:
			abspath = scene_name.abspath()
			return abspath
		elif basename:
			basename = scene_name.basename()
			return basename
		elif dir_base:
			dir_path = scene_name.dirname()
			basename = scene_name.basename()
			return [dir_path,basename]