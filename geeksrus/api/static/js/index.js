
$(function() {
    console.log( "ready!" );
          $('.carousel').carousel({
        interval: 2000
      });

    var color = d3.scale.category10();
    function tokenFreqSuccess(data, domPlaceHolder, type) {
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
          d3.select(domPlaceHolder).append("svg")
                  .attr("width", "100%")
                  .attr("height", 800)
                  .attr("class", "wordcloud")
                  .append("g")
                  // without the transform, words words would get cutoff to the left and top, they would
                  // appear outside of the SVG area
                  .attr("transform", "translate(435,325)")
                  .attr("text-anchor", "middle")
                  .selectAll("text")
                  .data(words)
                  .enter().append("text")
                  .style("font-size", function(d) { return d.size / 1.5+ "px"; })
                  .style("fill", function(d, i) { return color(i); })
                  .attr("transform", function(d) {
                      return "translate(" + [d.x / 1.2, d.y / 1.2 ] + ")rotate(" + d.rotate + ")";
                  })
                  .text(function(d) { return d.text; });
      }
  }

  //tokenFreqSuccess(window.cloudData, "#word-cloud-topics");
  //tokenFreqSuccess(window.cloudData1, "#word-cloud-mentions");
  $.get("/api/cloud/token", function(data){
    tokenFreqSuccess(data, "#word-cloud-topics");
  });

  $.get("/api/cloud/mentions", function(data){
    tokenFreqSuccess(data, "#word-cloud-mentions");
  });

  $.get("/api/cloud/users", function(data){
    tokenFreqSuccess(data, "#word-cloud-users");
  });

});
