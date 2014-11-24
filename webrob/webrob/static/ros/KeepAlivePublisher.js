
/**
 * Publishes keep alive message at regular intervals so that the
 * socket connection is not closed.
 */
function KeepAlivePublisher(options){
  var ros = options.ros;
  var interval = options.interval || 30000;
  
  console.log(ros);
  // The topic dedicated to keep alive messages
  var keepAliveTopic = new ROSLIB.Topic({
    ros : ros,
    name : '/keep_alive',
    messageType : 'std_msgs/Bool'
  });
  // A dummy message for the topic
  var keepAliveMsg = new ROSLIB.Message({
    data : true
  });
  // Function that publishes the keep alive message
  this.ping = function() {
    keepAliveTopic.publish(keepAliveMsg);
  };
  // Call ping at regular intervals.
  setInterval(this.ping, interval);
}
