## ������������ 3D ������ ��� ���������� �� ��������� ������������ ��� �������� ������


��� ��������� ����� �� ���� :

```
sudo apt update
sudo apt install python3-venv -y
python3 -m venv yolov8env
source yolov8env/bin/activate


pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

pip install ultralytics 

```

��� �� �� ����� ���������� ��� ��������� 

```
source yolov8env/bin/activate 
```

������ ��� ������ ��� ��� �� ������ .py �� ��� ������ ```cd```
��� ����� :

```
python detect.py
```

  <div style="text-align:center;">
    <img src="image/2.png" alt="1" width="800">
</div>


�  ����� :
```
python fasi1_detect_depth.py
```

  <div style="text-align:center;">
    <img src="image/3.png" alt="1" width="800">
</div>

� ����� :

```
python TELIKO_detect_depth_estimatinon.py
```

  <div style="text-align:center;">
    <img src="image/1.png" alt="1" width="800">
</div>