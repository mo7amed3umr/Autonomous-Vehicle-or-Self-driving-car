// //  const http = require('http');  
  
// // const port = 8080;  
  
// // const server = http.createServer((req, res) => {  
// //   res.statusCode = 200;  
// //   res.setHeader('Content-Type', 'text/plain');  
// //   res.end('Hello World\n');  
// // });  
express = require('express');
const app = express();
const videoPath = "firstVideo.mp4";

const { spawn } = require('child_process');
const bat = spawn('/home/menna/anaconda3/bin/python',['/home/menna/Downloads/python/server.py',videoPath]);
let direction;
bat.stdout.on('data', (data) => {
  console.log(data.toString());
  direction = data.toString();

});

  
bat.stderr.on('data', (data) => {
  console.error(data.toString());
});

bat.on('exit', (code) => {
  console.log(`Child exited with code ${code}`);
});

app.get('/', function(req, res){
    res.send(direction);
    });
   
app.listen(8080, () => {  
  console.log(`Server running at http://localhost:8080/`);  
});  
// var PythonShell = require('python-shell');

//     var options = {
//       mode: 'text',
//       pythonPath: 'C:/Users/EG/Anaconda3/python.exe', 
//       pythonOptions: ['-u'],
//       // make sure you use an absolute path for scriptPath
//       scriptPath: 'C:\\Users\\EG\\Desktop\\task3\\Peer-to-Peer-Cue-System-master\\server.js',
//       args: ['value1', 'value2', 'value3']
//     };

//     PythonShell.run('test.py', options, function (err, results) {
//       if (err) throw err;
//       // results is an array consisting of messages collected during execution
//       console.log('results: %j', results);
//     });
