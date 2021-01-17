# How to implement CRootLib inside Visual Studio

1. Copy the CRootLib folder inside Srcs/Client/
1. Inside VS: Solution menu -> Add -> Add existing solution -> CRootLib.vcxproj
1. Copy your python root files inside CRootLib/Workplace/Root
1. Run the Build -> Solution compilation to run the CRootLib pre-build event for cythonization
1. Add the generated .c files to the CRootLib project -> Add existing files [Preview](https://i.imgur.com/mqIR4UH.png)

### Common issues
#### Q: Nothing to do
A: If the cythonization event doesn't start, touch a random .cpp file and re-run the solution compilation.
