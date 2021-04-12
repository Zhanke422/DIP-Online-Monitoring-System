var express = require('express')
var server = express()

/* using files inside 'assets' folder */
server.use(express.static('assets'))

/* your landing page */
server.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

// server.get('/staff_1.html', (req, res) => {
//   res.sendFile(__dirname + '/staff_1.html');
// });

// server.get('/student_1.html', (req, res) => {
//   res.sendFile(__dirname + '/student_1.html');
// });

/* your port is localhost:8000 */
const port = 8000;

server.listen(port, function() {
  console.log('server listening on port ' + port)
})