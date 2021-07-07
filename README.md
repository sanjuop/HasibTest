Procedure for executing playblast scipt
1)Open the ABC_101_01_001_anim.ma file in maya
2)Execute the below lines in maya script editor
import sys
**path = r"D:\anim_test\Playblast"
sys.path.append(**path)
import playblast as pb;reload(pb)

---

Features that can be added

1. Tool can be docked
2. Can give extra options for user to select in UI like Frame range, camera etc
3. UI can be stylized using CSS
