filteredArray = []

function buildImages() {
    url = '/fetch/api'

    d3.json(url).then(data => {
        // d3.select(".image_container").remove()
        var input = d3.select("#input").property("value");
        var input2 = d3.select("#input2").property("value");
        var color_input = d3.select("#color").property("value");
        var inputs = [input, input2]
        filteredArray = data;
        // test if both inputs are empy to display blank page
        if (input === '' && input2 === '') {
            filteredArray = []
        }

        inputs.forEach( (filter, index) => {
            if (filter) {
                // filter based on class from user input
                filteredArray = filteredArray.filter((dict) => dict['classes_detected'].includes(filter));
                // filter out anything with a certainty less than 99%
                filteredArray = filteredArray.filter( (dict) => {
                    index_of_score = dict['classes_detected'].indexOf(filter);
                    return dict['scores'][index_of_score] > 0.99
                })
            }
        });

        // filteredArray = filteredArray.slice(2);
        // filteredArray = colorFilter(filteredArray);
        createImageDivs(filteredArray);

    });
}

function colorFilter() {

    var color_input = d3.select("#color").property("value");
    // filter for color
    switch(color_input) {
        case 'red':
            coloredArray = filteredArray.filter((dict) => dict['color_percentages'].red > 50);
          break;
        case 'blue':
            coloredArray = filteredArray.filter((dict) => dict['color_percentages'].blue > 50);
          break;
        case 'purple':
            coloredArray = filteredArray.filter((dict) => dict['color_percentages'].purple > 50);
          break;
        case 'orange':
            coloredArray = filteredArray.filter((dict) => dict['color_percentages'].orange > 50);
          break;
        default:
            coloredArray = filteredArray;
      }
      createImageDivs(coloredArray)
}

function createImageDivs(filteredArray) {
    d3.select(".image_container").remove()
        
    var container = d3.select("main")
                    .append("div")
                    .attr("class", "image_container container-fluid");

    container.selectAll('img')
        .data(filteredArray)
        .enter()
        .append('div')
        .attr('class','col')
        .append('div')
        .attr('class','thumbnail')
        .append('img')
        .attr('class', 'img-fluid img-thumbnail')
        .attr('src', d => d.image_url);
}

function buildPieChart(img_url) {

    var data = filteredArray.filter((dict) => dict.image_url === img_url);
    var colors = [];
    var values = [];
    var color_object = data[0]['color_percentages'];
    var colorData = {'colors': colors, 'values':values};


    Object.entries(color_object).forEach(([key,value]) => {
        colors.push(key);
        values.push(value);
    });
    

    var myDuration = 600;
    var firstTime = true;

    var width = 960,
    height = 500,
    radius = Math.min(width, height) / 2;

    var width = 960,
    height = 500,
    radius = Math.min(width, height) / 2;
    var color = d3.scaleOrdinal(d3.schemeCategory10);

    var pie = d3.pie()
        .value(function(d) { return colorData.values; })
        .sort(null);

    var arc = d3.arc()
        .innerRadius(radius - 100)
        .outerRadius(radius - 20);

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var colorsByValue = d3.nest()
        .key(function(d) { return colorData.colors; })
        .entries(colorData)
        .reverse();

    var label = d3.select("form").selectAll("label")
        .data(colorsByValue)
        .enter().append("label");

    label.append("input")
        .attr("type", "radio")
        .attr("name", "fruit")
        .attr("value", function(d) { return d.key; })
        .on("change", change)
        .filter(function(d, i) { return !i; })
        .each(change)
        .property("checked", true);

    label.append("span")
        .text(function(d) { return d.key; });

    function change(region) {
        var path = svg.selectAll("path");
        var data0 = path.data(),
        data1 = pie(region.values);

        path = path.data(data1, key);

        path
        .transition()
        .duration(myDuration)
        .attrTween("d", arcTween)


        path
        .enter()
        .append("path")
        .each(function(d, i) {
            var narc = findNeighborArc(i, data0, data1, key) ;
            if(narc) {          
            this._current = narc;
            this._previous = narc;
            } else {          
            this._current = d;
            }
        }) 
        .attr("fill", function(d,i) { 
        return color(d.data.region)
        })
        .transition()
        .duration(myDuration)
        .attrTween("d", arcTween)


        path
        .exit()
        .transition()
        .duration(myDuration)
        .attrTween("d", function(d, index) {

            var currentIndex = this._previous.data.region;
            var i = d3.interpolateObject(d,this._previous);
            return function(t) {
            return arc(i(t))
            }

        })
        .remove()
    }
    function key(d) {
        return d.data.region;
      }
    
      function type(d) {
        d.count = +d.count;
        return d;
      }
    
      function findNeighborArc(i, data0, data1, key) {
        var d;
        if(d = findPreceding(i, data0, data1, key)) {
    
          var obj = cloneObj(d)
          obj.startAngle = d.endAngle;
          return obj;
    
        } else if(d = findFollowing(i, data0, data1, key)) {
    
          var obj = cloneObj(d)
          obj.endAngle = d.startAngle;
          return obj;
    
        }
    
        return null
    
    
    }
    
    // Find the element in data0 that joins the highest preceding element in data1.
    function findPreceding(i, data0, data1, key) {
      var m = data0.length;
      while (--i >= 0) {
        var k = key(data1[i]);
        for (var j = 0; j < m; ++j) {
          if (key(data0[j]) === k) return data0[j];
        }
      }
    }
    
    // Find the element in data0 that joins the lowest following element in data1.
    function findFollowing(i, data0, data1, key) {
      var n = data1.length, m = data0.length;
      while (++i < n) {
        var k = key(data1[i]);
        for (var j = 0; j < m; ++j) {
          if (key(data0[j]) === k) return data0[j];
        }
      }
    }
    
    function arcTween(d) {
    
      var i = d3.interpolate(this._current, d);
    
      this._current = i(0);
    
      return function(t) {
        return arc(i(t))
      }
    
    }
    
    
    function cloneObj(obj) {
      var o = {};
      for(var i in obj) {
        o[i] = obj[i];
      }
      return o;
    }
}
// added a bunch of event listeners because I can't figure out which one works best
d3.select("#color").on("change", colorFilter);
// d3.select("body").on("click", colorFilter);


d3.select("body").on("keydown", buildImages);

d3.select("form").on("keydown", buildImages);

d3.select("html").on("keydown", buildImages);
d3.select("html").on("click", colorFilter);


// buildImages()