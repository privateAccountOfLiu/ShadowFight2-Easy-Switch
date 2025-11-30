# 暗影格斗2 简易转换器（中文版）

## 摘要
&emsp;&emsp;基于PySide6与Vtk的Python项目，可帮助您完成游戏相关文件的格式转换，为《ShadowFight2》提供更佳的游戏体验。

## 项目介绍
### 代码说明
&emsp;&emsp;项目提供了发行版EXE文件和一些源代码。若您希望直接使用本项目，只需下载发行版EXE文件并运行它（注意：程序将在其所在目录中新建三个文件夹作为输出文件夹）。
&emsp;&emsp;若您希望通过源代码运行程序，您仅需下载所有的Python代码，但需要你注意文件间的结构关系。您也可以直接克隆本项目到本地运行。在运行之前，您必须要安装依赖：
```
pip install pyside6 vtk
```
基于Qt框架的GUI程序：
直接运行`main.py`程序，这是我们的GUI入口，进入界面之后可以通过Qt控件选择所需功能。

### 功能1：模型转换
#### ModelEditor：支持.xml(游戏内模型)与.obj(WaveFront模型)：
&emsp;&emsp;通过此功能，您将可视化选中的模型，并且可以对模型进行一些整体性质和标签的修改，最终导出令你满意的模型文件，在常见的Wavefront模型（.obj文件）与《ShadowFight2》专用模型（.xml文件）之间建起一道格式转换的桥梁。

### 功能2：动作文件合并
#### 多obj数据转换为csv张量
&emsp;&emsp;将您的动作文件（大量.obj文件）反序列化，并以csv格式存储。

### 功能3：动作文件解码与编码
#### AnimationEditor
&emsp;&emsp;将二进制动作文件解码为csv表格存储格式，或将csv表格中的动作信息编码为《ShadowFight2》可识别的二进制文件，您可以在此功能中预览整个动作是如何工作的！

## 注意事项

### 本程序为开源项目，请勿用作商业活动！
***
# Shadow Fight 2 Simple Converter (English Version)  
## Abstract  
&emsp;&emsp;A Python project based on PySide6 and Vtk that helps you convert game-related files, providing an enhanced gaming experience for *Shadow Fight 2*.  

## Project Introduction  
### Code Description  
&emsp;&emsp;The project provides a release version of the EXE file and some source code. If you wish to use the project directly, simply download the release version of the EXE file and run it (Note: The program will create three new folders in its directory as output folders).  

&emsp;&emsp;If you wish to run the program from the source code, you only need to download all the Python code, but you must pay attention to the structural relationships between the files. You can also clone the project directly to run it locally. Before running, you must install the dependencies:  
```  
pip install pyside6 vtk  
```  
A GUI program based on the Qt framework:  
Run the `main.py` program directly. This is the entry point for our GUI. Once the interface is open, you can use Qt controls to select the desired functionality.  

### Feature 1: Model Conversion  
#### ModelEditor: Supports .xml (in-game models) and .obj (WaveFront models):  
&emsp;&emsp;With this feature, you can visualize the selected model and make modifications to its overall properties and labels. Finally, you can export the model file to your satisfaction, building a bridge for format conversion between common Wavefront models (.obj files) and *Shadow Fight 2* specific models (.xml files).  

### Feature 2: Motion File Merging  
#### Multi-obj Data Converted to CSV Tensor  
&emsp;&emsp;Deserialize your motion files (a large number of .obj files) and store them in CSV format.  

### Feature 3: Motion File Decoding and Encoding  
#### AnimationEditor  
&emsp;&emsp;Decode binary motion files into CSV table storage format, or encode motion information from CSV tables into binary files recognizable by *Shadow Fight 2*. With this feature, you can preview how the entire motion works!  

## Notes  
### This program is an open-source project and must not be used for commercial activities!