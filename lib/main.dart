import 'package:flutter/material.dart';
import 'package:smart_car_/automatic_mode.dart';
import 'package:camera/camera.dart';
import 'package:smart_car_/manual_mode.dart';
import 'package:http/http.dart' as http;

Future<void> main() async {
  // Ensure that plugin services are initialized so that `availableCameras()`
  // can be called before `runApp()`
  WidgetsFlutterBinding.ensureInitialized();
  // final CameraDescription camera;
  // Obtain a list of the available cameras on the device.
  final cameras = await availableCameras();
  // Get a specific camera from the list of available cameras.
  // final firstCamera = cameras.first;
  runApp(
    MaterialApp(
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        accentColor: Colors.black12,
      ),
      home: MyApp(cameras: cameras),
    ),
  );
}

class MyApp extends StatefulWidget {
  List<CameraDescription>? cameras;

  MyApp({Key? key, this.cameras}) : super(key: key);
  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> with TickerProviderStateMixin {
  TabController? tabController;
  var tabIndex = 0;

  List<Widget> tabs = [
    Tab(icon: Icon(Icons.camera)),
    Tab(icon: Icon(Icons.settings))
  ];

  late CameraController cameraController;
  late Future<void> initializeControllerFuture;

  @override
  void initState() {
    // // To display the current output from the Camera,
    //   cameraController = CameraController(
    //   // Get a specific camera from the list of available cameras.
    //   widget.firstCamera as CameraDescription,
    //   // Define the resolution to use.
    //   ResolutionPreset.medium,

    // // Next, initialize the controller. This returns a Future.
    // initializeControllerFuture = cameraController.initialize();
    tabController = TabController(length: 2, vsync: this);
    tabController!.addListener(() {
      setState(() {
        tabIndex = tabController!.index;
        print('index: $tabIndex');
      });
      var uri = Uri.parse('http://192.168.43.90/PostMode/');
      if (tabIndex == 0) {
        http.post(uri, body: {'mode': 'M'});
        print(tabIndex);
      } else {
        http.post(uri, body: {'mode': 'A'});
        print(tabIndex);
      }
    });

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      initialIndex: 1,
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Your Car Controller'),
          bottom: TabBar(
            controller: tabController,
            tabs: tabs,
          ),
        ),
        body: TabBarView(
          controller: tabController,
          children: <Widget>[
            ManualMode(),
            AutomaticMode(
              cameras: widget.cameras,
            ),
          ],
        ),
      ),
    );
  }
}
