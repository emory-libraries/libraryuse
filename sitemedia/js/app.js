App = Ember.Application.create({
  LOG_TRANSITIONS:true
});


App.Router.map(function() {
  this.resource('index', { path: '/' });
  // this.route('catchall', {path: '/*wildcard'});
  this.resource('library', { path: '/library' },function(){
    this.route('test');
    this.route('test1');
    this.route('test2');
    this.route('all');
    this.route('woodruff');
    this.route('business');
    this.route('health-science');
    this.route('law');
  });
  this.resource('lib', { path: '/library/:lib' });

  this.resource('demo', { path: '/library/:lib/:category/:demo'});

  this.resource('date', { path: '/library/:lib/:category/:demo/:date'});


  this.resource('reports', { path: 'reports' });
  this.resource('json');
  // this.route("fourOhFour", { path: "*path"});
});



App.classificationsStore = Ember.Object.extend({});

var test = 'nope';

$.ajax({
  url: '/classifications',
  dataType: 'jsonp',
  jsonpCallback:'jsonResponse',
  success:function(data){
    test = data;
  }
});

App.ApplicationRoute = Ember.Route.extend({
  model: function() {
    return Ember.$.getJSON('/classifications')
  },
  actions:{
    error: function () {
      this.transitionTo('catchall', "application-error");
    }
  }
});

var GLOBAL_LIB='';

App.FilterButtonComponent = Ember.Component.extend({
  layoutName:"components/filter-button"
});

App.StudentsFilterButtonComponent = Ember.Component.extend({
  layoutName:"components/filter-button",
  addon: 'students'
});

App.FacultyFilterButtonComponent = Ember.Component.extend({
  layoutName:"components/filter-button",
  addon: 'faculty'
});


App.IndexRoute = Ember.Route.extend({
  model: function() {
    return ['red','green','purple']
  },
  setupController: function(controller,model) {
    this._super(controller, model);
    controller.set('title', "My App");
  },
  activate: function() {
        $(document).attr('title', 'My App');
    },
  beforeModel: function() {
      this.transitionTo('library.all');
  }
});



App.reportStore = Ember.Object.extend({});



App.ReportsRoute = Ember.Route.extend({
  model: function(params) {
    return Ember.$.getJSON('/top_dprtn/woodruff/2013-8-28/2014-8-28/')
  }
});


//LIBRARY ROOT
App.LibraryRoute = Ember.Route.extend({
  activate: function() {
    var title = $(document).attr('title');
    $(document).attr('title', title+'-Library');
  },
  setupController: function(controller) {
    controller.set('title', "Library");
  }
});


App.urlStore = Ember.Object.extend({
  paths: null,
  names: null,
  category:null
});
var dataURL = App.urlStore.create();

var libList = App.urlStore.create();


//ALL LIBS
App.LibraryAllRoute = Ember.Route.extend({
  model:function(){
     var data = {
              title: 'All Libraries'
            }
        dataURL.set('names', [
          'Woodruff',
          'Health Sciences',
          'Law'
          ]);
        dataURL.set('paths', [
          'woodruff',
          'health',
          'law'
          ]);
     return data;
  },
  renderTemplate: function() {
      this.render('library/libraries');
      $(document).attr('title', "Libraries");              
  }
});

//LIB ROOT
App.LibRoute = Ember.Route.extend({
    model:function(params){
      var libs = params.libs;
      if(libs.indexOf('woodruff')>-1){
        var data = {
              title: 'Woodruff',
              student_info:[1,2,3]
            }
        dataURL.set('names', [data.title]);
        dataURL.set('paths', ["woodruff"]);
      }
      else if(libs.indexOf('health-science')>-1){
        var data = {
              title: 'Health Science',
              student_info:[1,2,3]
            }
        dataURL.set('names', [data.title]);
        dataURL.set('paths', ["health-science"]);
      }
      else if(libs.indexOf('law')>-1){
        var data = {
              title: 'Law',
              student_info:[1,2,3]
            }
        dataURL.set('names', [data.title]);
        dataURL.set('paths', ["law"]);
      }

      return data;
    },
    renderTemplate: function() {
      this.render('library/libraries');
    $(document).attr('title', "Woodruff"); 
  }
});

function getLibName(path){
  var url = path,
      libList = ['all','woodruff','health-science','law'],
      libNameList = ['All', 'Woodruff','Health Science','Law'],
      libName = 'all';
  $.each(libList,function(i){
    if(path.indexOf(libList[i])>0){
      libName = libNameList[i];
    }
  })
  return libName;
}


function setJsonParams(options){
    var library_name = options.lib,
        library_category = options.cat,
        library_student_class = options.studclass;

}


//DEMOGRAPHIC ROOT
App.DemoRoute = Ember.Route.extend({
  model:function(params){
    var data = {demo:params.demo, category:params.category};
    // console.log(params)
    return data;
  },
  afterModel: function (model){
    _this = this;
    var library_name = getLibName(_this.get('router.url'));

    var library_path = getLibPath(library_name);
    GLOBAL_LIB = library_name
    $(document).attr('title', library_name); 

    function getLibPath(name){
      return name.replace(' ','-').toLowerCase();
    }

    if(library_path=='all'){
      dataURL.set('names', ['Woodruff','Health Sciences','Law']);
        dataURL.set('paths', ['woodruff','health','law']);
    }
    else{
      dataURL.set('names', [library_name]);
      dataURL.set('paths', [library_path]);
    }
    
    if(model.category=='students'){
      model.category = 'student_class';
    }
    else if(model.category=='faculty'){
      model.category = 'faculty_staff_class';
    }
    else{

    }

    dataURL.set('category',[model.category])

    dataURL.set('group',[model.demo])


  },
  renderTemplate: function() {
      this.render('library/libraries');
  }
});


//Date ROOT
App.DateRoute = Ember.Route.extend({
  model:function(params){
    var date = params.date;
    console.log(date);
  },
  afterModel: function (model){
    _this = this;
    var library_name = getLibName(_this.get('router.url'));

    Ember.run.next(function(){
    });
  }
});

//Woodruff
App.LibraryWoodruffRoute = Ember.Route.extend({
  model:function(){

     var data = {
          title: 'Woodruff'
        }
        dataURL.set('names', [data.title]);
        dataURL.set('paths', ["woodruff"]);
        dataURL.set('category',['total_usage'])
        dataURL.set('group',[''])
     return data;
  },
  renderTemplate: function() {
      this.render('library/libraries');
    $(document).attr('title', "Woodruff"); 
  }
});

App.LibraryWoodruffView = Ember.View.create({
  init:function(){

  }
});


//Business
App.LibraryBusinessRoute = Ember.Route.extend({
  model:function(){
     var data = {
              title: 'Business',
              student_info:['Freshman','Sophomore','Junior','Senior'],
              faculty_info:['Faculty','Staff','Temp'],
              dept_info:['Dept1','Dept2','Dept3'],
              acad_info:['Acad1','Acad2','Acad3']
              }
        dataURL.set('names', [data.title]);
        dataURL.set('paths', ["woodruff"]);
        dataURL.set('category',['total_usage'])
        dataURL.set('group',[''])
     return data;
  },
  renderTemplate: function() {
      this.render('library/libraries');
      $(document).attr('title', "Business");         
  }
});

App.LibraryBusinessView = Ember.View.create({
  init:function(){
    
  }
});

//Health Sciences
App.LibraryHealthScienceRoute = Ember.Route.extend({
  model:function(){
     var data = {
              title: 'Health Sciences',
              student_info:['Freshman','Sophomore','Junior','Senior'],
              faculty_info:['Faculty','Staff','Temp'],
              dept_info:['Dept1','Dept2','Dept3'],
              acad_info:['Acad1','Acad2','Acad3']
                }
          dataURL.set('names', [data.title]);
          dataURL.set('paths', ['health-science']);
          dataURL.set('category',['total_usage'])
          dataURL.set('group',[''])
     return data;
  },
  renderTemplate: function() {
      this.render('library/libraries');
      $(document).attr('title', "Health Science");
  }
});

//Law
App.LibraryLawRoute = Ember.Route.extend({
  model:function(){
     var data = {
              title: 'Law',
              student_info:['Freshman','Sophomore','Junior','Senior'],
              faculty_info:['Faculty','Staff','Temp'],
              dept_info:['Dept1','Dept2','Dept3'],
              acad_info:['Acad1','Acad2','Acad3']
            }
      dataURL.set('names', [data.title]);
      dataURL.set('paths', ["law"]);
      dataURL.set('category',['total_usage'])
      dataURL.set('group',[''])
     return data;
  },
  renderTemplate: function() {
      this.render('library/libraries');
      $(document).attr('title', "Law");            
  }
});

App.LibraryLawView = Ember.View.create({
  init:function(){
    
  }
});


App.NavView = Ember.View.extend({
  templateName: "lib-navigation",
  navItems: [
    {name:'All Libraries',path:'library.all', change:{value:'2%',net_class:'text-success'}},
    {name:'Woodruff',path:'library.woodruff', change:{value:'2%',net_class:'text-success'}},
    {name:'Health Science',path:'library.health-science', change:{value:'12%',net_class:'text-success'}},
    {name:'Law',path:'library.law', change:{value:'4%',net_class:'text-success'}},
  ],
  didInsertElement : function(){
      var that = this;
      Ember.run.next(function(){

        new mlPushMenu( document.getElementById( 'mp-menu' ), document.getElementById( 'trigger' ) );
      });
    }
});

App.NetChangeComponent = Ember.Component.extend({
  didInsertElement:function(){
    
  }
});

var selection = []

// function that builds both the charts on the Library pages
function SUPERCHART(url){
    var path = dataURL.get('paths'),
        d = '',
        uri_category = dataURL.get('category') || 'total_usage',
        uri_users = dataURL.get('group') || '';

      uri_category+='/';
      
      if(uri_users.length>1){
        uri_users='/'+uri_users+'/';
      }

    function formatDate(date){
      var formatted_date = (date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate())
      return formatted_date;
    }

    var $container = $('#container'),
      seriesOptions = [],
      yAxisOptions = [],
      seriesCounter = 0,
      enableLegend =false,
      names = dataURL.get('names'),
      // colors = Highcharts.getOptions().colors;
      colors= ['#FB715E','#7994FF','#5AA689','#FFD340','#796499'],
      uri_path = '/',
      today = new Date(), 
      monthsAgo = 6,
      start_date = new Date(today.getFullYear(), today.getMonth()-monthsAgo, today.getDate());
      date_range = '/'+formatDate(start_date)+'/'+formatDate(today)+'/';

    $.each(names, function(i, name) {

      console.log(path[i])
      console.log(uri_path+uri_category+path[i]+uri_users+date_range);

      $.ajax({
          url: uri_path+uri_category+path[i]+uri_users+date_range,
          dataType: 'json',
          success:function(data){jsonResponse(data)},
          error: function(xhr, status, error){
            console.log(xhr.responseText)
            var $error = $('<div/>').attr({'class':'error-loading'}).append('<span/>').html("<p>Sorry, it's taking a while to load.</p>");
            $error.append($("<a/>").attr({'href':'#','class':'btn btn-warning btn-refresh'}).append('Refresh'));
            $container.html($error);
            $error.fadeOut(0).fadeIn(500)
            $(document).on('click','.btn-refresh',function(evt){
              evt.preventDefault();
              location.reload(true);
            })
          }
        });


        function jsonResponse(data) {
          d = data;
          if(data.data !== undefined){
            d = data.data;
          }
          else{
            d = data;
          }
          // console.log(name)
          var color = colors[i];

          if(name=='Woodruff'){
            color='#FB715E';
          }
          if(name=='Law'){
            color='#7994FF';
          }
          if(name=='Health Sciences'||name=='Health Science'){
            color='#5AA689';
          }

          if(d.length!==0){

            seriesOptions[i] = {
              name: name,
              id: name,
              data: d,
              color:color,
              fillColor : {
                linearGradient : {
                  x1: 0, 
                  y1: 0, 
                  x2: 0, 
                  y2: 1
                },
                stops : [
                  [0, 'rgb(65, 73, 85)'], 
                  [1, 'rgb(65, 73, 85)']
                ]
              },
              pointInterval: 36 * 1000
            };

            // As we're loading the data asynchronously, we don't know what order it will arrive. So
            // we keep a counter and create the chart when all the data is loaded.
            seriesCounter++;

            if (seriesCounter == names.length) {
             //  Timeline Events are possible!
              // seriesOptions.push(
              // {
              //     name : "Flaged Events", 
              //     color: '#999',
              //     type : 'flags',
              //     data : [
              //       {
              //         x : 1405536180000,      // Point where the flag appears
              //         title : 'Timeline Event 1', // Title of flag displayed on the chart 
              //         text : 'Description for timeline event.'   // Text displayed when the flag are highlighted.
              //       },
              //       {
              //         x : 1407272940000,      // Point where the flag appears
              //         title : 'Timeline Event 2', // Title of flag displayed on the chart 
              //         text : 'Description for timeline event.'   // Text displayed when the flag are highlighted.
              //       }
              //     ],
              //     onSeries : '',  // Id of which series it should be placed on. If not defined 
              //                     // the flag series will be put on the X axis
              //     shape : 'flag'  // Defines the shape of the flags.
              // });
              drawChart(seriesOptions);
              drawChartLastWeek(seriesOptions);
            }
          }
          else{
            console.log('There are no returns for this category in '+name+'.');
          }
        }

        function drawChartLastWeek(data){
          var $container = $('#container-lastweek'),
              enableLegend = (data.length > 1 ? true : false);
          Highcharts.setOptions({
              global: {
                  timezoneOffset: 5 * 60
              }
          });
          $container.highcharts('StockChart', {
            chart:{
              backgroundColor:'transparent',
              type:'column'
            },
            rangeSelector: {
                  buttons: [{
                    type: 'day',
                    count: 1,
                    text: '1d'
                  },{
                    type: 'day',
                    count: 3,
                    text: '3d'
                  },{
                    type: 'week',
                    count: 1,
                    text: '1w'
                  }],
                  selected: 0,
                },

            yAxis: {
                labels: {
                    formatter: function() {
                        return (this.value < 0 ? '-' : '') + Highcharts.numberFormat(this.value, 0);;
                    }
                },
                floor:0
            },
            navigator : {
              enabled : false
            },
            scrollbar : {
              enabled : false
            },
            plotOptions: {
                series: {
                    compare: undefined, //value, percent
                    dataGrouping:{
                      approximation:'sum',
                      smoothed:false,
                      forced:true,
                      units: [ ['hour', [1]] ]  
                    }
                }
            },
            legend: {
              enabled: enableLegend,
            },
            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y} patrons</b><br/>',
                changeDecimals: 2,
                valueDecimals: 0
            },
            inputDateFormat: '%H:%M:%S.%L',
            inputEditDateFormat: '%H:%M:%S.%L',
            // Custom parser to parse the %H:%M:%S.%L format
            inputDateParser: function(value) {
                value = value.split(/[:\.]/);
                return Date.UTC(
                    1970, 
                    0, 
                    1, 
                    parseInt(value[0]),
                    parseInt(value[1]),
                    parseInt(value[2]),
                    parseInt(value[3])
                );
            },

            title: {
                text: '',
                floating: true
            },
            
            xAxis: {
                tickPixelInterval: 120,
                type: 'datetime',
                dateTimeLabelFormats : {
                    hour: '%I %p',
                    minute: '%I:%M %p'
                },
            },
            series: data
          }, function(chart) {
              // apply the date pickers
            setTimeout(function(){
                $($('#'+chart.options.chart.renderTo.id + ' input.highcharts-range-selector'))
                .datepicker({
                    beforeShow: function(i,obj) {
                        $widget = obj.dpDiv;
                        window.$uiDatepickerDiv = $widget;
                        $uiDatepickerDiv.addClass("ll-skin-melon");
                        if ($widget.data("top")) {
                            setTimeout(function() {
                                $uiDatepickerDiv.css( "top", $uiDatepickerDiv.data("top") );
                            },50);
                        }
                    }
                    ,onClose: function(i,obj) {
                        $widget = obj.dpDiv;
                        $widget.data("top", $widget.position().top);
                    }
                })
            },0)
          });//end highcharts
        }//end drawChartLastWeek

        function drawChart(data){
          var $container= $('#container'),
              enableLegend = (data.length > 1 ? true : false);
          Highcharts.setOptions({
              global: {
                  timezoneOffset: 5 * 60
              }
          });
          $container.highcharts('StockChart', {
            chart:{
              backgroundColor:'transparent'
            },
            rangeSelector: {
                  buttons: [{
                    type: 'week',
                    count: 1,
                    text: '1w'
                  }, {
                    type: 'month',
                    count: 1,
                    text: '1m'
                  }, {
                    type: 'month',
                    count: 3,
                    text: '3m'
                  }, {
                    type: 'month',
                    count: 6,
                    text: '6m'
                  }, {
                    type: 'ytd',
                    text: 'YTD'
                  }, {
                    type: 'year',
                    count: 1,
                    text: '1y'
                  }, {
                    type: 'all',
                    text: 'All'
                  }],
                  selected: 1,
                  inputDateFormat: '%b %e %Y',
                  inputEditDateFormat: '%Y-%m-%d' 
                },

            yAxis: {
                labels: {
                    formatter: function() {
                        return (this.value < 0 ? '-' : '') + Highcharts.numberFormat(this.value, 0);;
                    }
                },
                floor:0
            },
            legend: {
              enabled: enableLegend,
            },
            plotOptions: {
                series: {
                    compare: undefined, //value, percent
                    dataGrouping:{
                      approximation:'sum',
                      smoothed:false,
                      forced:false,
                      groupPixelWidth:300,
                      units: [ ['minute',[15]],['hour', [1]],['day',[1]] ]
                    },

                }
            },
            
            tooltip: {
                pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y} patrons</b><br/>',
                changeDecimals: 2,
                valueDecimals: 0
            },
            
            title: {
                text: '',
                floating: true
            },
            
            xAxis: {
                tickPixelInterval: 120,
                type: 'datetime',
                dateTimeLabelFormats : {
                    hour: '%I %p',
                    minute: '%I:%M %p'
                },
            },
            series: data
          }, function(chart) {
              // apply the date pickers
            setTimeout(function(){
                $('#'+chart.options.chart.renderTo.id+' input.highcharts-range-selector')
                .datepicker({
                    beforeShow: function(i,obj) {
                        $widget = obj.dpDiv;
                        window.$uiDatepickerDiv = $widget;
                        $uiDatepickerDiv.addClass("ll-skin-melon");
                        if ($widget.data("top")) {
                            setTimeout(function() {
                                $uiDatepickerDiv.css( "top", $uiDatepickerDiv.data("top") );
                            },50);
                        }
                    }
                    ,onClose: function(i,obj) {
                        $widget = obj.dpDiv;
                        $widget.data("top", $widget.position().top);
                    }
                })

                // Set the datepicker's date format
                $.datepicker.setDefaults({
                    dateFormat: 'yy-mm-dd',
                    onSelect: function(dateText) {
                        this.onchange();
                        this.onblur();
                    }
                });
            },0)
          });//end highcharts
        }//end drawChart

    })//end $.each
}//end SUPERCHART


App.JsonChartComponent = Ember.Component.extend({
  didInsertElement: function(url){

    function setTab(hash){
      var path =hash.split('/');
      var $libTabs = $('.nav-reports .list-group-item');
      var libTabNames = {
        "all":0,
        "woodruff":1,
        "health-science":2,
        "law":3
      }
      var selectedLibTab = libTabNames[path[2]];
      $libTabs.removeClass('active');
      $($libTabs[selectedLibTab]).addClass('active');
    }

    function updateFilterLinks(hash){
      var path = hash;
      $(".mp-menu ul li > a").each(function(){

        path = hash.split('/');

        var $this = $(this),
            category = $this.parents('ul').first().attr('class')||'other',
            newURL = path[0]+"/"+path[1]+"/"+path[2]+"/"+category+"/"+$this.text();
          $this.attr('href',newURL);
      });

      setTab(hash);

      if($('.mp-pusher').hasClass("mp-pushed")){
        SUPERCHART(url);
      }
    }

    

    var hash = window.location.hash
    SUPERCHART(url);
    updateFilterLinks(hash);
    $(window).hashchange( function(){

      updateFilterLinks(hash);
      
    });
  }//end didInsertElement
});


//Loading Component
App.FlipLoadingComponent = Ember.Component.extend({
  didInsertElement:function(){
    var clock;
    
    $(document).ready(function() {
      var clock;

      clock = $('.clock').FlipClock(0, {
            clockFace: 'Counter',
            countdown: false,
        });
        setTimeout(function() {
        setInterval(function() {
          clock.increment();
        }, 1000);
      });

    });
  }
});


