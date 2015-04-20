var graph;
var step;
var data;
var WAITMSEC = 100;

function pracGraph(el) {

this.addNode = function (id) {
  nodes.push({"id":id});
  update();
};


this.updateData = function (data) {
  var tmpNodes = [];
  var nodesCopy = [];
  var r = $.Deferred(),
      r2 = $.Deferred();

  // create temporary 
  for (var a in data) {
    if (typeof findNodeInList(data[a].source, tmpNodes) === "undefined") {
      tmpNodes.push(data[a].source);
    }
    if (typeof findNodeInList(data[a].target, tmpNodes) === "undefined") {
      tmpNodes.push(data[a].target);
    }
  }

  // add all nodes and links
  var addnodesandlinks = function(a) {
    var aInterval = setTimeout( function() {
    if (typeof findNode(data[a].source) === "undefined") {
      nodes.push({"id":data[a].source});
    }
    if (typeof findNode(data[a].target) === "undefined") {
      nodes.push({"id":data[a].target});
    }
    links.push({"source":findNode(data[a].source),"target":findNode(data[a].target),"value":data[a].value});
    update();
    a++;
    if (a >= data.length) {
      nodesCopy = nodes.slice();
      r.resolve();
    } else {
      addnodesandlinks(a);
    }
  }, WAITMSEC);
  return r;
  };


  // remove all nodes and links, that are not in the new data
  var removenodes = function(r) {
    var rInterval = setTimeout( function() {
      if (!nodeInList(nodesCopy[r].id, tmpNodes)) {
        // this.removeNode(nodes[r].id);
        var i = 0;
        var n = findNode(nodesCopy[r].id);
        while (i < links.length) {
          if ((links[i]['source'] == n)||(links[i]['target'] == n))
          {
            links.splice(i,1);

          }
          else i++;
        }
        nodes.splice(findNodeIndex(nodesCopy[r].id),1);
        setTimeout( function() { update(); }, WAITMSEC);
      }
      r++;
      if (r >= nodesCopy.length) {
        r2.resolve();
      } else {
        removenodes(r);
      }
    }, WAITMSEC);
  };

  addnodesandlinks(0).done(function() { 
    removenodes(0); 
  });
  
};

var nodeInList = function(id, n) {
  for (var i in n) {
    if (n[i] === id) {
      return true;
    }
  }
  return false;
};


var findNodeInList = function(id, n) {
  for (var i in n) {
    if (i.id === id) return i;};
};


this.removeNode = function (id) {
  var i = 0;
  var n = findNode(id);
  while (i < links.length) {
    if ((links[i]['source'] == n)||(links[i]['target'] == n))
    {
      links.splice(i,1);
    }
    else i++;
  }
  nodes.splice(findNodeIndex(id),1);
};

this.removeLink = function (source,target){
  for(var i=0;i<links.length;i++)
  {
    if(links[i].source.id == source && links[i].target.id == target)
    {
      links.splice(i,1);
      break;
    }
  }
  update();
};

this.removeallLinks = function(){
  links.splice(0,links.length);
  update();
};

this.removeAllNodes = function(){
  nodes.splice(0,nodes.length);
  update();
};

this.clear = function() {
  this.removeallLinks();
  this.removeAllNodes();
}

this.addLink = function (source, target, value) {
  links.push({"source":findNode(source),"target":findNode(target),"value":value});
  update();
};

this.showlinks = function() {
  for (var l = 0; l < links.length; l++) {
    alert(links[l].source.id + " " + links[l].target.id + " " + links[l].value);
  }
};

this.showNodes = function(n) {
  alert('adding string');
  var str = '';
  for (var l = 0; l < n.length; l++) {
    str += n[l].id;
    str += ", ";
  }
  alert(str);
};

var findNode = function(id) {
  for (var i in nodes) {
    if (nodes[i].id === id) return nodes[i];};
};

var findNodeIndex = function(id) {
  for (var i=0;i<nodes.length;i++) {
    if (nodes[i].id==id){
      return i;
    }
  };
};

var w = $('#viz').width(),
    h = $('#viz').height();

var svnContainer = d3.select('#viz')
  .append("svg:svg")
  .attr("width", w)
  .attr("height", h)
  .attr("id","svg")
  .append('svg:g');

svnContainer.append("defs").selectAll("marker")
  .data(["dashedred", "strokegreen", "dashed", "strokeblue"])
  .enter().append("marker")
  .attr("id", function(d) { return d; })
  .attr("viewBox", "0 -5 10 10")
  .attr("refX", 15)//15
  .attr("refY", -1.5)
  .attr("markerWidth", 6)
  .attr("markerHeight", 6)
  .attr("orient", "auto")
  .append("path")
  .attr("d", "M0,-5L10,0L0,5");
  // .attr("d", "M 0,0 V 4 L6,2 Z");

var force = d3.layout.force();

var nodes = force.nodes(),
    links = force.links();

var update = function () {
  var path = svnContainer.selectAll("path.link")
    .data(links, function(d) {
            return d.source.id + "-" + d.target.id; 
            });


  var pathEnter = path.enter().append("path")
  // path.enter().append("path")
    .attr("id", function(d) { return d.source.id + "-" + d.target.id; })
    // .attr("class", function(d) { return "link"; })
    .attr("class", function(d) { return "link " + d.value; })
    .attr("marker-end", function(d) { return "url(#" + d.value + ")"; });

  path.exit().remove();

  var circle = svnContainer.selectAll("g.node")
    .data(nodes, function(d) { return d.id; } );

  var circleEnter = circle.enter().append("g")
    .attr("class", "node")
    .call(force.drag);

  circleEnter.append("svg:circle")
    .attr("r", 6)
    .attr("id", function(d) { return d.id; } );

  // circleEnter.append("svg:rect")
  //   .attr("width", function(d) {return 15*d.id.length;}) // set width according to text length
  //   .attr("height", 25)
  //   .attr("id", function(d) { return d.id; } );

  circleEnter.append("svg:text")
    .attr("class","textClass")
    .attr("dx", function (d) { return 5 }) // move inside rect
    .attr("dy", function (d) { return 15 }) // move inside rect
    .text( function(d) { return d.id; } );

  circle.exit().remove();

  this.tick = function () {
    circle.attr("transform", transform);
    path.attr("d", linkArc);
  }

  this.linkArc = function (d) {
    var dx = d.target.x - d.source.x,
        dy = d.target.y - d.source.y,
        dr = Math.sqrt(dx * dx + dy * dy);
    return "M" + 
        d.source.x + "," + 
        d.source.y + "A" + 
        dr + "," + dr + " 0 0,1 " + 
        d.target.x + "," + 
        d.target.y;
  }

  this.transform = function (d) {
    return "translate(" + d.x + "," + d.y + ")";
  }

  force
  .size([w, h])
  .linkDistance( h/6 )
  .charge(-300)
  .on("tick", tick)
  .gravity( .03 )
  .distance( 150 )
  .start();
};


// Make it all go
update();
}

function loadGraph(steps) {
  console.log(steps);
  step = 0;
  data = [];

  // create javascript dict from inference result
  for (var key in steps) {
    if (steps.hasOwnProperty(key)) {
      var stp = steps[key];
      links = [];
      for (var y = 0, link; y < stp.length; y++) {
        link = stp[y];
        links.push({source: link['source'], target: link['target'], value: link['value']});
      }
      data.push(links);
    }
  }

  if (typeof graph === 'undefined') {
    graph = new pracGraph("#viz");
  } else {
    graph.clear();
  }
  drawGraph();

}

function drawGraph() {
  if (step < data.length) {
    graph.updateData(data[step]);
    step++;
  }
  else {
    alert("No more steps");
  }
}


function clearGraph() {
  step = 0;
  graph.clear();
}

// window.onload = initGraph();