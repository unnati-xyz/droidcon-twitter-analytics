
$(function() {
    console.log( "ready!" );
          $('.carousel').carousel({
        interval: 10000
      });

    var color = d3.scale.category10();
    function tokenFreqSuccess(data, domPlaceHolder, type) {
      $(domPlaceHolder).html("");
      d3.layout.cloud().size([1600, 600])
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
                  .attr("height", 400)
                  .attr("class", "wordcloud")
                  .append("g")
                  // without the transform, words words would get cutoff to the left and top, they would
                  // appear outside of the SVG area
                  .attr("transform", "translate(400,200)")
                  .attr("text-anchor", "middle")
                  .selectAll("text")
                  .data(words)
                  .enter().append("text")
                  .style("font-size", function(d) { return d.size / 2.5+ "px"; })
                  .style("fill", function(d, i) { return color(i); })
                  .attr("transform", function(d) {
                      return "translate(" + [d.x / 2, d.y / 2 ] + ")rotate(" + d.rotate + ")";
                  })
                  .text(function(d) { return d.text; });
      }

  }

  function renderTweetStream(data) {
    var htmlString = "";
    var height = $("#tweets-list").height();

    var template = '<div class="row">\
                <div class="col-md-11 well">\
                  <div class="row">\
                    <div class="col-md-3"><img src={{dp}}></div>\
                    <div class="col-md-9">\
                      <div class="row">\
                        <span class="screen-name">{{name}}</span>\
                      </div>\
                      <div class="row">\
                        <span class="handle">@{{screen_name}}</span>\
                      </div>\
                    </div>\
                  </div>\
                  <div class="row tweet-text">{{text}}</div>\
                </div>\
            </div>';

/*
    var template = '<div class="row"> \
      <div class="col-md-11 well"> \
        <div class="row"> \
          <div class="col-md-3"><img src={{dp}}></div>\
          <div class="col-md-9">\
          <div class="row">\
          <span class="screen-name">{{name}}</span> \
          </div>\
          <div class="row">\
          <span class="handle">@{{screen_name}}</span> \
          </div>\
        </div> \
        <div class="row tweet-text">{{text}}</div> \
      </div> \
    </div>';
   */

    for(var i=0; i<data.length; i++) {
        var output = Mustache.render(template, data[i]);
        htmlString += output;
    }

    $("#tweets-list").append(htmlString);
    $('.sidebar').animate({scrollTop: height}, 500);

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

  function pollTweetStream() {
    $.ajax({
        url: "/api/timeline",
        type: "GET",
        success: renderTweetStream,
        complete: setTimeout(function(){pollTweetStream()}, 5000)
      });
  };

  function pollTopTopics() {
    $.ajax({
        url: "/api/cloud/token",
        type: "GET",
        success: function(data) {
            tokenFreqSuccess(data, "#word-cloud-topics");
        },
        complete: setTimeout(function(){pollTopTopics()}, 5000)
      });
  };

  function pollTopMentions() {
    $.ajax({
        url: "/api/cloud/mentions",
        type: "GET",
        success: function(data) {
            tokenFreqSuccess(data, "#word-cloud-mentions");
        },
        complete: setTimeout(function(){pollTopMentions()}, 5000)
      });
  };

  pollTweetStream();
  pollTopTopics();
  pollTopMentions();

});

