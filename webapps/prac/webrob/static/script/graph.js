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
    links.push({"source":findNode(data[a].source),"target":findNode(data[a].target),"value":data[a].value, "arcStyle":data[a].arcStyle});
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

this.addLink = function (source, target, value, arcStyle) {
  links.push({"source": findNode(source),"target": findNode(target),"value": value,"arcStyle": arcStyle});
  update();
};

this.showlinks = function() {
  for (var l = 0; l < links.length; l++) {
    alert(links[l].source.id + " " + links[l].target.id + " " + links[l].value + " " + links[l].arcStyle);
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
  .data(["dashedred", "strokegreen", "dashed", "strokeblue", "arrowhead", "default"])
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
  console.log(graph);
  var path = svnContainer.selectAll("path.link")
    .data(links, function(d) {
            return d.source.id + "-" + d.target.id; 
            });

  var pathEnter = path.enter().append("path")
    .attr("id", function(d) { return d.source.id + "-" + d.target.id; })
    .attr("class", function(d) { return "link " + d.value; })
    .attr("marker-end", function(d) { return "url(#" + d.arcStyle + ")"; });

  path.exit().remove();

  var edgelabels = svnContainer.selectAll(".label")
        .data(links, function(d) {
            return d.source.id + "-" + d.target.id; 
            });

  var edgelabelsEnter = edgelabels.enter().append('text')
      .style("pointer-events", "none")
      .attr('class', 'label')
      .text(function(d){return d.value});

  edgelabels.exit().remove();

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
    .attr("dx", function (d) { return 5; }) // move inside rect
    .attr("dy", function (d) { return 15; }) // move inside rect
    .text( function(d) { return d.id; } );

  circle.exit().remove();


  this.tick = function () {
    path.attr("d", linkArc);
    edgelabels.attr('d', linkArc);
    edgelabels.attr('transform', rotateLabel);
    edgelabels.attr('x', transformLabelX);       
    edgelabels.attr('y', transformLabelY);       
    circle.attr("transform", transform);
  }

  this.rotateLabel = function (d) {
    // if (d.target.x<d.source.x){
            bbox = this.getBBox();
            rx = bbox.x+bbox.width/2;
            ry = bbox.y+bbox.height/2;
            var dX = d.target.x - d.source.x;
            var dY = d.target.y - d.source.y;
            var rad = Math.atan2(dX, dY);
            var deg = -90-rad * (180 / Math.PI);
            return 'rotate(' + deg +' '+rx+' '+ry+')';
  }


  this.linkArc = function (d) {
    var dx = d.target.x - d.source.x,
        dy = d.target.y - d.source.y,
        dr = Math.sqrt(dx * dx + dy * dy);
    return "M" + 
        d.source.x + "," + 
        d.source.y + "A" + 
        dr + "," + dr + " 0 0,0 " + 
        d.target.x + "," + 
        d.target.y;
  }

  // move arc label to arc
  this.calcLabelPos = function (d, bbox) {
    var scale = 0.3;
    var origPos = { x: (d.source.x + d.target.x ) /2 - bbox.width/2, y: (d.source.y + d.target.y) /2 }; // exact middle between source and target
    var dir = { x: d.target.x - d.source.x, y: d.target.y - d.source.y }; // direction source -> target
    var rot = { x: dir.y, y: -dir.x }; // rotate direction -90 degrees
    var length = Math.sqrt(rot.x * rot.x + rot.y * rot.y) / 100 // normalize length
    var rotNorm = { x: rot.x / length, y: rot.y / length }; // normalize rotation direction
    return { x: origPos.x - scale * rotNorm.x, y: origPos.y - scale * rotNorm.y};// return moved position
  }

  this.transform = function (d) {
    return "translate(" + d.x + "," + d.y + ")";
  }

  this.transformLabel = function (d) {
    return "translate(" + d.source.x + "," + d.source.y + ")";
  }

  this.transformLabelX = function (d) {
    bbox = this.getBBox();
    return calcLabelPos(d, bbox).x;
  }

  this.transformLabelY = function (d) {
        bbox = this.getBBox();
    return calcLabelPos(d, bbox).y;
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
        links.push({source: link['source'], target: link['target'], value: link['value'], arcStyle: link['arcStyle']});
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
