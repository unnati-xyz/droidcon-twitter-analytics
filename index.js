
$(function() {
    console.log( "ready!" );

    var color = d3.scale.category10();
    window.cloudData = [
  {
    "size": 68,
    "text": "addyosmani"
  },
  {
    "size": 69,
    "text": "chunking"
  },
  {
    "size": 35,
    "text": "audience"
  },
  {
    "size": 18,
    "text": "per"
  },
  {
    "size": 35,
    "text": "always"
  },
  {
    "size": 69,
    "text": "Architecture"
  },
  {
    "size": 69,
    "text": "Universal"
  },
  {
    "size": 70,
    "text": "Progressive"
  },
  {
    "size": 69,
    "text": "App"
  },
  {
    "size": 37,
    "text": "conference"
  },
  {
    "size": 179,
    "text": "jsfoo"
  },
  {
    "size": 76,
    "text": "Slides"
  },
  {
    "size": 18,
    "text": "route"
  },
  {
    "size": 18,
    "text": "sharding"
  },
  {
    "size": 18,
    "text": "html"
  },
  {
    "size": 31,
    "text": "organised"
  },
  {
    "size": 31,
    "text": "speak"
  },
  {
    "size": 32,
    "text": "slides"
  },
  {
    "size": 31,
    "text": "attentive"
  },
  {
    "size": 32,
    "text": "treat"
  },
  {
    "size": 51,
    "text": "_abhinavrastogi"
  },
  {
    "size": 18,
    "text": "bundle"
  },
  {
    "size": 69,
    "text": "PRPL"
  },
  {
    "size": 31,
    "text": "well"
  },
  {
    "size": 69,
    "text": "AppShell"
  },
  {
    "size": 69,
    "text": "based"
  },
  {
    "size": 72,
    "text": "Web"
  },
  {
    "size": 71,
    "text": "Rendering"
  },
  {
    "size": 21,
    "text": "talk"
  },
  {
    "size": 20,
    "text": "Flipkart"
  },
  {
    "size": 17,
    "text": "samccone"
  },
  {
    "size": 69,
    "text": "Route"
  },
  {
    "size": 18,
    "text": "sF2PuLOMEj"
  },
  {
    "size": 18,
    "text": "push"
  },
  {
    "size": 69,
    "text": "Webpack"
  },
  {
    "size": 18,
    "text": "streaming"
  }
];
  function tokenFreqSuccess(data) {
      $("#word-cloud").html("");
      d3.layout.cloud().size([1200, 600])
              .words(data)
              .rotate(0)
              .fontSize(function(d) { return d.size; })
              .padding(5)
              .spiral("archimedean")
              //.rotate(function() { return ~~(Math.random() * 2) * 90; })
              .on("end", draw)
              .start();

      function draw(words) {
          d3.select("#word-cloud-topics").append("svg")
                  .attr("width", "100%")
                  .attr("height", 400)
                  .attr("class", "wordcloud")
                  .append("g")
                  // without the transform, words words would get cutoff to the left and top, they would
                  // appear outside of the SVG area
                  .attr("transform", "translate(335,225)")
                  .attr("text-anchor", "middle")
                  .selectAll("text")
                  .data(words)
                  .enter().append("text")
                  .style("font-size", function(d) { return d.size / 2 + "px"; })
                  .style("fill", function(d, i) { return color(i); })
                  .attr("transform", function(d) {
                      return "translate(" + [d.x / 1.75, d.y / 1.75 ] + ")rotate(" + d.rotate + ")";
                  })
                  .text(function(d) { return d.text; });
      }
  }

  tokenFreqSuccess(window.cloudData);

});
