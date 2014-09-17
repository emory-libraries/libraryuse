App = Ember.Application.create({
  LOG_TRANSITIONS:true
});


App.Router.map(function() {
  this.resource('index', { path: '/' });
  // this.route('catchall', {path: '/*wildcard'});
  this.resource('library', { path: '/library' },function(){
    this.route('all');
    this.route('woodruff');
    this.route('business');
    this.route('health-science');
    this.route('law');
    
    this.resource('lib', { path: '/:lib' });
    
    this.resource('demo', { path: '/:lib/:category/:demo'});
    
    this.resource('date', { path: '/:lib/:category/:demo/:date'});
  });
  this.resource('reports', { path: 'reports' },function(){
    this.route('reports-index');
    this.resource('report', { path: '/:id' });
    this.resource('report', { path: '/:id/:lib' });
    
    this.resource('today-report', { path: '/:id/:lib/:start' });
    this.resource('report', { path: '/:id/:lib/:start/:end' });
  });
  
  this.resource('averages', { path: 'total_averages' },function(){
    this.route('averages-index');
    this.resource('avg-report', { path: '/:lib/:start/:end/:time1/:time2/:dow' });  
  });
  
  
  this.resource('json');
  // this.route("fourOhFour", { path: "*path"});
});



App.classificationsStore = Ember.Object.extend({});

App.ApplicationRoute = Ember.Route.extend({
  model: function() {
    return Ember.$.getJSON('/classifications')
  }
});

App.ApplicationController = Ember.Controller.extend({
  actions:{
    error: function () {
      this.transitionTo('catchall', "application-error");
    }
  }
})


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
  },
  setupController: function(controller,model) {
    // controller.set('title', "My App");
  },
  activate: function() {
    // $(document).attr('title', 'My App');
  },
  beforeModel: function() {
    this.transitionTo('library.all');
  }
});

App.reportsStore = Ember.Object.extend({
  id: undefined,
  lib: undefined,
  start: undefined,
  end:undefined
});

var reportParams = App.reportsStore.create();


App.urlStore = Ember.Object.extend({
  paths: null,
  names: null,
  category:null,
  start:null,
  end:null,
  distinct:null,
  campus:null
});
//This sets the default globals
var today = new Date(), 
monthsAgo = 2,
default_start = new Date(today.getFullYear(), today.getMonth()-monthsAgo, today.getDate()),
default_end = today;

var dataURL = App.urlStore.create({
  start:default_start,
  end:default_end,
  distinct:false,
  time1:0,
  time2:23,
  dow:1
});

var libList = App.urlStore.create();

function setGlobalReportVariables(_var, value, _this,route){
  reportParams.set(_var, value)
  loadReport(_this,route);
}

function convertDate(d) {
  if (typeof d == "string" || d ==undefined){
    return d;
  }
  var yyyy = d.getFullYear().toString();                                    
  var mm = (d.getMonth()+1).toString(); // getMonth() is zero-based         
  var dd  = d.getDate().toString();             
  
  return yyyy + '-' + (mm[1]?mm:"0"+mm[0]) + '-' + (dd[1]?dd:"0"+dd[0]);
}

function loadReport(_this, route){
  var id = reportParams.get("id"),
  lib = reportParams.get('lib'),
  start = convertDate(dataURL.get('start')),
  end = convertDate(dataURL.get('end')),
  time1 = reportParams.get('time1'),
  time2 = reportParams.get('time2'),
  dow = reportParams.get('dow'),
  route = (route==undefined) ? "report" : "averages";
  
  var link = '/'+id+'/'+lib+'/'+start+'/'+end,
  name = "Report: "+id+"|"+lib+"|"+start+"|"+end;
  $("#report-chart .loading-data").show();


  if(route=="averages"){
    _this.transitionToRoute("avg-report",lib,start,end,time1,time2,dow)
  }
  else{  
    _this.transitionToRoute(route,id,lib,start,end)
  }
}

App.CalendarDatePicker = Ember.TextField.extend({
  _picker: null,
  
  modelChangedValue: function(){
    // console.log('inside CalendarDatePicker'+this.get("value"))
  }.observes("value"),
  
  didInsertElement: function(){
    var formatted_start = convertDate(reportParams.get("start"))
    var formatted_end = convertDate(reportParams.get("end"))
    
    
    var defaults = {
      id: "top_academic_plan",
      lib: "woodruff",
    }
    
    var urlDate = {
      start:  formatted_start,
      end: formatted_end
    }
    
    $(".report-dates.inputs>form>input")
    .datepicker({
      beforeShow: function(i,obj) {
        $widget = obj.dpDiv;
        window.$uiDatepickerDiv = $widget;
        $uiDatepickerDiv.addClass("ll-skin-melon").addClass("report-dates");
        if ($widget.data("top")) {
          setTimeout(function() {
            $uiDatepickerDiv.css( "top", $uiDatepickerDiv.data("top") );
          },50);
        }
      },
      maxDate: new Date,
      dateFormat: "m/d/yy",
      onClose: function(i,obj) {
        $widget = obj.dpDiv;
        $widget.data("top", $widget.position().top);
      }
    });
    
    $(".report-dates.inputs>form>input.start")
    .datepicker("setDate", new Date(urlDate.start));
    
    $(".report-dates.inputs>form>input.end")
    .datepicker("setDate", new Date(urlDate.end))
  }
});



App.ReportsIndexRoute = Ember.Route.extend({
  redirect : function(){
    var defaults = {
      id: "top_academic_plan",
      lib: "woodruff",
      start:  formatDate(dataURL.get("start")),
      end: formatDate(dataURL.get("end"))
    }
  
    $(".global-loading").hide();
    this.transitionTo("report", defaults.id,defaults.lib,defaults.start,defaults.end);
  }
});

App.AveragesIndexRoute = Ember.Route.extend({
  redirect : function(){
    var defaults = {
      id: "total_averages",
      lib: "woodruff",
      start:  formatDate(dataURL.get("start")),
      end: formatDate(dataURL.get("end")),
      time1: dataURL.get("time1"),
      time2: dataURL.get("time2"),
      dow: dataURL.get("dow")
    }
    
    $(".global-loading").hide();
    this.transitionTo("avg-report", defaults.lib,defaults.start,defaults.end,defaults.time1,defaults.time2,defaults.dow);
  }
});

App.ReportsRoute = App.AveragesRoute = Ember.Route.extend({
  model: function(params) {
    $(document).attr('title', "Reports");
    Ember.run.next(this, function(){ 
      $(".loading-data").hide();
      $(".load-date").removeClass('disabled');
    });
  }
});

App.ReportRoute = App.AvgReportRoute = Ember.Route.extend({
  model: function(params) {
    var defaults = this.get("defaults");

    if(params.id && params.id!="undefined"){
      reportParams.set('id',params.id);
    }
    else{
      reportParams.set('id',defaults.id);
    }
    
    if(params.lib && params.lib!="undefined"){
      reportParams.set('lib',params.lib);
    }
    else{
      reportParams.set('lib',defaults.lib);
    }
    
    if(params.start && params.start!="undefined"){
      reportParams.set('start',params.start);
    }
    else{
      reportParams.set('start',defaults.start);
    }
    
    if(params.end && params.end!="undefined"){
      reportParams.set('end',params.end);
    }
    else{
      reportParams.set('end',defaults.end);
    }
    
    if(params.time1 && params.time1!="undefined"){
      reportParams.set('time1',params.time1);
    }
    else{
      reportParams.set('time1',defaults.time1);
    }
    
    if(params.time2 && params.time2!="undefined"){
      reportParams.set('time2',params.time2);
    }
    else{
      reportParams.set('time2',defaults.time2);
    }
    
    if(params.dow && params.dow!="undefined"){
      reportParams.set('dow',params.dow);
    }
    else{
      reportParams.set('dow',defaults.dow);
    }
    
    var id = reportParams.get("id"),
    lib = reportParams.get('lib'),
    start = convertDate(reportParams.get('start')),
    end = convertDate(reportParams.get('end')),
    time1 = reportParams.get('time1'),
    time2 = reportParams.get('time2'),
    dow = reportParams.get('dow');
    
    var jsonUrl = "/"+id+"/"+lib;
    
    if(id == "on_off_campus" ){
      jsonUrl += "/"+"Y";
    }
    
    if(id =="faculty_divs_dprt"){
      Ember.run.next(function(){
        $(".extended-load").show();
      })
    }
    
    jsonUrl += "/"+start+"/"+end+"/";

    if(this.routeName=="avg-report"){
      jsonUrl += time1+"/"+time2+"/";
    }
    
    $(document).attr('title', "Reports|"+" "+lib+ ": "+id );
    if(this.routeName=="avg-report"){
      return jsonUrl+"?querytime="+Math.round(new Date().getTime() / 1000)
    }
    else{
      // jsonUrl = "/static/js/data/test-divs.json";
      return Ember.$.getJSON(jsonUrl)
    }
  }
});

App.ReportRoute = App.ReportRoute.extend({
  defaults:{
    id: "top_academic_plan",
    lib: "woodruff",
    start:  dataURL.get("start"),
    end: dataURL.get("end"),
    time1: 12,
    time2: 13,
    dow: 1
  },
  renderTemplate:function(){
    if(reportParams.get("id")=="on_off_campus"){
      this.render('report-campus')
    }
    else{
      this.render('report');
    }
  }
})


App.AveragesRoute = App.AveragesRoute.extend({
  renderTemplate:function(){
    this.render('averages');
  }
});

App.AvgReportRoute = App.AvgReportRoute.extend({
  defaults:{
    id: "total_averages",
    lib: "woodruff",
    start:  dataURL.get("start"),
    end: dataURL.get("end"),
    time1: 12,
    time2: 13,
    dow: 1
  },
  renderTemplate:function(){
    this.render('avg-report');
  }
})



App.ReportsController = Ember.Controller.extend({
  default_lib: function(){
    return reportParams.get('lib')
  }.property(),
  
  lib: function(){
    return this.get("default_lib")
  }.property(),
  
  isWoodruff:function(){
    if(this.get("lib")=="woodruff"){
      return true
    }
  }.property("lib"),
  
  isHealth:function(){
    if(this.get("lib")=="health"){
      return true
    }
  }.property("lib"),
  
  isLaw:function(){
    if(this.get("lib")=="law"){
      return true
    }
  }.property("lib"),
  
  default_id: function(){
    return reportParams.get('id')
  }.property(),
  
  id:function(){
    return this.get("default_id")
  }.property(),
  
  isCampus:function(){
    if(this.get("id")=="on_off_campus"){
      return true
    }
  }.property("id"),
  
  isDiv:function(){
    if(this.get("id")=="faculty_divs_dprt"){
      $(".extended-load ").show();
      return true
    }
  }.property("id"),
  
  isAcad:function(){
    if(this.get("id")=="top_academic_plan"){
      return true
    }
  }.property("id"),
  
  isDprt:function(){
    if(this.get("id")=="faculty_divs_dprt"){
      return true
    }
  }.property("id"),
  
  startDateInput: "",
  
  endDateInput: "",
  
  actions:{
    setLibrary: function(libName) {
      this.set('lib', libName)
      $('#report-chart .chart').css('opacity',0)
      setGlobalReportVariables('lib',libName, this)
    },
    
    setType: function(idName) {
      this.set('id', idName)
      $('#report-chart .chart').css('opacity',0)
      setGlobalReportVariables('id',idName, this)
    },
    
    loadDates: function() {
      var newdate ={
        start: this.get("startDateInput") || dataURL.get('start'),
        end: this.get("endDateInput") || dataURL.get('end')
      },
      olddate = {
        start: dataURL.get('start'),
        end: dataURL.get('end')
      }
      
      if(newdate.start.length>0){
        newdate.start = newdate.start.split('/');
        newdate.start = new Date(newdate.start[2],newdate.start[0]-1,newdate.start[1])
      }
      if(newdate.end.length>0){
        newdate.end = newdate.end.split('/');
        newdate.end = new Date(newdate.end[2],newdate.end[0]-1,newdate.end[1])
      }
      
      if(olddate.start!==newdate.start || olddate.end!==newdate.end){
        //Update the datepicker on the options sidebar manually
        $(".options-date-range .form-group>input.start").datepicker("setDate",newdate.start)
        $(".options-date-range .form-group>input.end").datepicker("setDate",newdate.end)
        
        //Upadte the global url settings
        dataURL.set('start',newdate.start);
        dataURL.set('end',newdate.end);
        
        //Hide and Show the loading indicators
        $(".loading-data").not('.page-level').show();
        $(".load-date").addClass('disabled');
        $('#report-chart .chart').css('opacity',0)
        
        loadReport(this);
      }
    }
  }
});

App.ReportController = Ember.Controller.extend({
  theFilter: "",
  
  numberToShow: 20,
  
  formattedDate: function(){
    var start = this.get("model.meta.strt_date"),
    end = this.get("model.meta.end_date")
    
    function rearrangeDate(str){
      str = str[0]
      if (typeof str == "string"){
        str = str.split('-');
        str = str[1]+"/"+str[2]+"/"+str[0]
      }
      return str;
    }
    
    return {"start":rearrangeDate(start), "end":rearrangeDate(end)}
  }.property("model.meta.strt_date", "model.meta.end_date"),
  
  placeholder: function(){
    return ("Filter by "+ this.get("model.meta.title")[0]+"s")  
  }.property('model.meta.title'),
  
  firstItemInArray: function() {
    var data = this.get('model.data');
    var report_type = reportParams.get('id');

    if(report_type=='faculty_divs_dprt'){
      data = this.get('model.data.divs');
    }
      // console.log(data)
    
    return data.filter( function(item, index) {
      // return true if you want to include this item
      // for example, with the code below we include all but the first item
      if (index == 0) { 
        return item;     
      }    
    });
  }.property('model.data.@each'),
  
  filteredSum: function(){
    var sum = 0;
    this.get('filterPeople').filter( function(_this, index) {
      sum+=parseInt(_this.value) 
    })
    return sum;
  }.property('filterPeople'),
  
  filterPeople: function() { 
    var searchText = this.get('theFilter').toLowerCase(),
    exclude = searchText.indexOf('!')==0,
    n = this.get('numberToShow');
    
    if(exclude){
      searchText=searchText.substring(1)
    }
    if(this.get('model.average')){
      return this.get('model.average')
    }
    
    var data;
    var report_type = reportParams.get('id');
    
    if(report_type=='faculty_divs_dprt'){
      data = this.get('model.data.divs')
    }
    else{
      data = this.get('model.data')
    }
    
    return data.filter( function(_this, index) {
      // return true if you want to include this item
      // for example, with the code below we include all but the first item
      
      if(_this.label){
        var item = _this.label.toLowerCase();
        if(item.indexOf(searchText)>-1 && !exclude){
          return item
        }
        else if(item.indexOf(searchText)!==0 && exclude){
          return item
        }
      }
    });
    
    return
    
  }.property("theFilter","model.data.@each"),
  
  drawPieChart: (function(){
    var total_sum = this.get('filteredSum'),
    n = this.get('numberToShow'),
    datapoints = [],
    drilldown = [],
    drilldownSeries = [],
    allothers = 0;
    
    this.get('filterPeople').filter( function(_this, index) {
      var label = "'"+_this.label+"'",
      percent = parseInt((_this.value/total_sum *100).toPrecision(3));
      if(index<n){
        var point = {
                      name: label,
                      y: percent,
                      drilldown: label
                    }
                    
        if(_this.depts && _this.depts.length>0){
          var data =[]
          for (var i=0; i<_this.depts.length; i++){
            var dept = _this.depts[i];
            data.push([dept.label,parseInt(dept.value)])
          }
          drilldownSeries.push({ 
            id: label,
            name: label,
            data: data
          })
          
        }
                    
        datapoints.push(point)
      }
      else{
        drilldown.push(label);
        allothers+=percent
      }
    });
    
    if( drilldown.length>1){
      drilldown=['All Others',allothers];
      datapoints.push(drilldown);
    }
    
    function capitaliseFirstLetter(string)
    {
      return string.charAt(0).toUpperCase() + string.slice(1);
    }
    
    var byFilter =this.get("theFilter");
    if(byFilter.length>0){
      if(byFilter.indexOf('!')==0){
        byFilter = " when excluding: "+ byFilter.substring(1);
      }
      else{
        byFilter = " when filtered by: "+ byFilter;
      }
    }
    
    var library_name = this.get("model.meta.library")[0],
    report_title = this.get("model.meta.title")[0],
    total = this.get("filteredSum");
    
    function draw(){
      Highcharts.setOptions({
        lang: {
          drillUpText: '<< Back to all divisions'
        }
      });
      $('#report-chart .chart').highcharts({
        chart: {
          backgroundColor:'transparent',
          plotBackgroundColor: null,
          plotBorderWidth: 1,
          plotBorderColor: 'transparent',
          plotShadow: false,
          type: "pie"
        },
        title: {
          text: capitaliseFirstLetter(library_name) + 
          ' Vistors per '+report_title+" (Total: "+total+") "+byFilter
        },
        tooltip: {
          pointFormat: '{series.name}: <b>{point.percentage:.2f}%</b>',
        },
        navigation: {
            buttonOptions: {
                theme: {
                    'stroke-width': 0,
                    stroke: "#DCDEE5",
                    r: 3,
                    style:{
                      'cursor':"pointer"
                    },
                    states: {
                        hover: {
                            fill: '#DCDEE5'
                        },
                        select: {
                            stroke: '#DCDEE5',
                            fill: '#DCDEE5'
                        }
                    }
                }
            }
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: true,
              format: '<b>{point.name}</b>: {point.percentage:.1f}%',
              style: {
                color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
              }
            }
          }
        },
        series: [{
          type: 'pie',
          name: '% visitors',
          data: datapoints
        }],
        drilldown: {
          activeDataLabelStyle: {
              textDecoration: 'none'
          },
          drillUpButton: {
            theme: {
              fill: 'transparent',
              'stroke-width': 1,
              stroke: '#6481DB',
              style: {
                  color:"#6481DB",
                  cursor:"pointer"
              },
              r: 2,
              states: {
                  hover: {
                      fill: '#6481DB',
                      style: {
                         color:"#FFF",
                    }
                  },
                  select: {
                      fill: '#6481DB',
                      style: {
                         color:"#FFF",
                       }
                  }
              }
            }
          },
          series: drilldownSeries,
        }
      }).css('opacity',1);
      $(".loading-data, .extended-load").hide();
      $(".load-date").removeClass('disabled');
    }
    Ember.run.once(this,function(){
      Ember.run.next(this, function(){ 
        window.setTimeout(draw,500)
        $('#report-chart').affix({
          offset: {
            top: $('#report-chart').offset().top
            , bottom: function () {
              return (this.bottom = $('.footer').outerHeight(true))
            }
          }
        });
      })
    })
  }).property("filterPeople"),
    
  drawCampusChart: (function(){
    var data = this.get("model.data"),
    name = this.get("model.meta.title");
    
    var id = reportParams.get("id"),
    lib = reportParams.get('lib'),
    start = convertDate(reportParams.get('start')),
    end = convertDate(reportParams.get('end'));
    
    var jsonUrl = "/on_off_campus/"+lib;
    jsonUrl += "/"+"N";
    jsonUrl += "/"+start+"/"+end+"/"
    
    var oc_data=""
    
    function draw(){
      Highcharts.setOptions({
        global: {
          useUTC: false
        }
      });
      $('#report-chart .chart')
      .highcharts('StockChart', {
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
          selected: 6,
          inputDateFormat: '%b %e %Y',
          inputEditDateFormat: '%Y-%m-%d' 
        },
        
        yAxis: {
          labels: {
            formatter: function() {
              return (this.value < 0 ? '-' : '') + Highcharts.numberFormat(this.value, 0);
            }
          },
          floor:0
        },
        
        title: {
          text: '',
          floating: true
        },
        
        series : [{
          name : "On Campus",
          data : data,
          color:{
            color:"rgb(59, 197, 83)",
            linearGradient: { x1: 1, x2: 0, y1: 0, y2: 0 },
            stops: [
            [0, 'rgb(59, 197, 83)'],
            [1, 'rgb(129, 231, 147)']
            ]
          },
          pointInterval: 36 * 1000
        },
        {
          name : "Off Campus",
          data : oc_data,
          color:{
            color:"rgb(255,130,87)",
            linearGradient: { x1: 1, x2: 0, y1: 0, y2: 0 },
            stops: [
            [0, 'rgb(255,130,87)'],
            [1, 'rgb(255,180,154)']
            ]
          },
          pointInterval: 36 * 1000
        }
        ],
        
        tooltip: {
          useHTML: true,
          borderWidth: 0,
          borderColor:null,
          backgroundColor:'#888',
          shadow: false,
          style: {
            padding: 0,
            borderRadius:'5px'
          },
          pointFormat: '<span style="color:{series.color.color}">{series.name}</span>: <b>{point.y} patrons</b><br/>',
          changeDecimals: 2,
          valueDecimals: 0
        },
        plotOptions: {
          series: {
            compare: undefined, //value, percent
            dataGrouping:{
              approximation:'sum',
              smoothed:false,
              forced:true,
              groupPixelWidth:300,
              units: [ ['minute',[15]],['hour', [1]],['day',[1]] ]
            }
          }
        },
        xAxis: {
          tickPixelInterval: 120,
          type: 'datetime',
          dateTimeLabelFormats : {
            hour: '%I %p',
            minute: '%I:%M %p'
          },
        }
      },
      function(chart) {
        // apply the date pickers
        setTimeout(function(){
          $(".loading-data").hide();
          $(".load-date").removeClass('disabled');
          $('#report-chart .chart input.highcharts-range-selector')
          .datepicker({
            beforeShow: function(i,obj) {
              $widget = obj.dpDiv;
              window.$uiDatepickerDiv = $widget;
              $uiDatepickerDiv.addClass("ll-skin-melon").removeClass("report-dates")
              if ($widget.data("top")) {
                setTimeout(function() {
                  $uiDatepickerDiv.css( "top", $uiDatepickerDiv.data("top") );
                },50);
              }
            },
            minDate: new Date(dataURL.get('start')),
            maxDate: new Date(dataURL.get('end')),
            onClose: function(i,obj) {
              $widget = obj.dpDiv;
              $widget.data("top", $widget.position().top);
            },
            dateFormat: 'yy-mm-dd',
            onSelect: function(dateText) {
              this.onchange();
              this.onblur();
            }
          });
        },0)
      })//end highstocks
      .css('opacity',1);
    }
    
    $.getJSON(jsonUrl,function(data){
      oc_data =  data.data;
      Ember.run.once(this,function(){
        Ember.run.next(this, function(){ 
          window.setTimeout(draw,500)
        });
      });
    })
    
  }).property("model.data")
  
});

App.AveragesController = Ember.Controller.extend({
  default_lib: function(){
    return reportParams.get('lib')
  }.property(),
  
  lib: function(){
    return this.get("default_lib")
  }.property(),
  
  isWoodruff:function(){
    if(this.get("lib")=="woodruff"){
      return true
    }
  }.property("lib"),
  
  isHealth:function(){
    if(this.get("lib")=="health"){
      return true
    }
  }.property("lib"),
  
  isLaw:function(){
    if(this.get("lib")=="law"){
      return true
    }
  }.property("lib"),
  
  actions:{
    setLibrary: function(libName) {
      this.set('lib', libName)
      // $('#averages-chart').css('opacity',0)
      
      setGlobalReportVariables('lib',libName, this,"averages")
    },
    
    setType: function(idName) {
      this.set('id', idName)
      // $('#averages-chart').css('opacity',0)
      setGlobalReportVariables('id',idName, this,"averages")
    },
    
    loadDatesAverages: function() {

      var newdate ={
        start: this.get("averagesStart") || dataURL.get('start'),
        end: this.get("averagesEnd") || dataURL.get('end')
      },
      olddate = {
        start: dataURL.get('start'),
        end: dataURL.get('end')
      }
      
      if(newdate.start.length>0){
        newdate.start = newdate.start.split('/');
        newdate.start = new Date(newdate.start[2],newdate.start[0]-1,newdate.start[1])
      }
      if(newdate.end.length>0){
        newdate.end = newdate.end.split('/');
        newdate.end = new Date(newdate.end[2],newdate.end[0]-1,newdate.end[1])
      }
      
      if(olddate.start!==newdate.start || olddate.end!==newdate.end){
        //Update the datepicker on the options sidebar manually
        $(".report-dates>input.start").datepicker("setDate",newdate.start)
        $(".report-dates>input.end").datepicker("setDate",newdate.end)
        
        //Upadte the global url settings
        dataURL.set('start',newdate.start);
        dataURL.set('end',newdate.end);
        
        var link = "#/total_averages/"+reportParams.get("lib")+"/"+convertDate(dataURL.get("start"))+"/"+convertDate(dataURL.get("end"))+"/"+reportParams.get("time1")+"/"+reportParams.get("time2")+"/"+reportParams.get("dow");
        
        window.history.pushState("Total Averages", "Total Averages", link);
        
        //Hide and Show the loading indicators
        $(".loading-data").not('.page-level').show();
        $(".load-date").addClass('disabled');
        $('#report-chart .chart').css('opacity',0)
        
        loadReport(this, "avg-report");
      }
    }
  }
});


App.HourPicker = Ember.TextField.extend({
  hours: ["12AM","1AM","2AM","3AM","4AM","5AM","6AM","7AM","8AM","9AM","10AM","11AM",
          "12PM","1PM","2PM","3PM","4PM","5PM","6PM","7PM","8PM","9PM","10PM","11PM"],
          
  modelChangedValue: function(){
    
    function convert12to24(str){
      var hour = parseInt(str),
          isAM =  str.indexOf("AM")>-1
      
      if(!isAM && hour!==12){
        hour+=12;
      }
      else if(isAM && hour==12){
        hour = 0;
      }
      
      return hour
    }
    
    var t1 = convert12to24($(".timepicker.start").val())
    var t2 = convert12to24($(".timepicker.end").val())
    reportParams.set("time1",t1)
    reportParams.set("time2",t2)

    loadReport(this._parentView.controller, "avg-report");
  }.observes("value"),
  
  didInsertElement: function(){
    $("#averages-chart input.timepicker").timepicker({
      beforeShow: function(i,obj) {
        $widget = obj.dpDiv;
        window.$uiDatepickerDiv = $widget;
        $uiDatepickerDiv.addClass("ll-skin-melon").addClass("report-dates").addClass("timepicker");
        if ($widget.data("top")) {
          setTimeout(function() {
            $uiDatepickerDiv.css( "top", $uiDatepickerDiv.data("top") );
          },50);
        }
      },
      showMinute:false,
      showTime:false, 
      timeFormat:"h TT",
      onClose: function(i,obj) {
        $widget = obj.dpDiv;
        $widget.data("top", $widget.position().top);
      }
    })
  }
});

App.AvgReportController = Ember.Controller.extend({
  formattedTime: function(){
    function formatTime(h){
      h = parseInt(h);
      var dd = "AM";
      
      if (h >= 12) {
        h = h-12;
        dd = "PM";
      }
      if (h == 0) {
          h = 12;
      }
      return h+" "+dd;
    }
    
    var start = formatTime(this.get("model.start_hour"))
    var end = formatTime(this.get("model.end_hour"))
    
    return {"start":start,"end":end}
    
  }.property("model.start_hour","model.end_hour"),
  
  drawAverages: function(){
    $(".global-loading").hide();
    $('#averages-chart .loading-data').show()
    $('#averages-chart .chart').css("opacity",0.2);
    var total_averages = this.get("model.data.average")
    
    var jsonUrl = this.get("model"),
        queryStr = jsonUrl.indexOf("?");
    
    if(queryStr>-1){
      jsonUrl = jsonUrl.substring(0,queryStr);
    }

    function draw(){
      $('#averages-chart .loading-data').show()
      var $container = $('#averages-chart .chart');
      
      var d=1,
          seriesOptions =[],
          seriesCounter=0,
          names = ["Sunday","Monday","Tuesday","Wednesday","Thrusday","Friday","Saturday"];
          
      $.each(names, function(i, name) {
        var requestURL = jsonUrl+(i+1)+"/";
        
        // console.log(requestURL);
        
        var json = $.getJSON(requestURL)
        
        json.done(function(data){
          if(data.data.average.length>0){
            jsonResponse(data)
          }
          else {
            data.data.average.push(0);
            console.log("This is empty.")
            jsonResponse(data)
          }
        })
        
        json.fail(function(){
          console.log('Error: JSON Ajax function failed.')
          var $error = $('<div/>').attr({'class':'error-loading'}).append('<span/>').html("<p>Sorry, the data failed to load from the server.</p>");
          $container.html($error);
          $error.fadeOut(0).fadeIn(500);
          dataURL.set("drawing","")
        });
        
        function jsonResponse(data) {
          d = data;
          if(data.data !== undefined){
            d = data.data;
          }
          else{
            d = data;
          }
          
          seriesOptions[i] = {
            name: name,
            data: [parseInt(d.average)],
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
            events: {
              legendItemClick:function(){
                // this.chart.redraw();
              }
            }
          };
          
          // As we're loading the data asynchronously, we don't know what order it will arrive. So
          // we keep a counter and create the chart when all the data is loaded.
          seriesCounter++;
          
          if (seriesCounter == names.length) {
            chartAverages(seriesOptions);
            dataURL.set("drawing",false)
          }
        }
      })
      
      
      function chartAverages(seriesOptions){
        $(".loading-data").hide();
        $(".load-date").removeClass('disabled');

        $('#averages-chart .counter').animateNumber({ number: total_averages });
        var $container = $('#averages-chart .chart'),
        enableLegend = true;
        Highcharts.setOptions({
          global: {
            useUTC: false
          }
        });
        $container.highcharts({
          chart:{
            backgroundColor:'transparent',
            type:'column'
          },
          navigation: {
              buttonOptions: {
                  theme: {
                      'stroke-width': 0,
                      stroke: "#DCDEE5",
                      r: 3,
                      style:{
                        'cursor':"pointer"
                      },
                      states: {
                          hover: {
                              fill: '#DCDEE5'
                          },
                          select: {
                              stroke: '#DCDEE5',
                              fill: '#DCDEE5'
                          }
                      }
                  }
              }
          },
          xAxis: {
            categories: ['Average'],
            labels: {enabled:false}
          },
          yAxis: {
            title:{text:"Number of patrons"},
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
          legend: {
            enabled: enableLegend,
          },
          tooltip: {
            useHTML: true,
            borderWidth: 0,
            borderColor:null,
            backgroundColor:'#888',
            shadow: false,
            style: {
              padding: 0,
              borderRadius:'5px'
            },
            pointFormat: '<span>{series.name}</span>: <b>{point.y} patrons</b><br/>',
            changeDecimals: 2,
            valueDecimals: 0
          },
          
          title: {
            text: '',
            floating: true
          },
          
          plotOptions: {
            series: {
              animation: false,
              borderWidth: 0,
              pointWidth: 20
            }
            
          },
          
          series: seriesOptions
        });//end highcharts
        $('#averages-chart .chart').css("opacity",1)
      }
    }
      Ember.run.next(this, function(){ 
        window.setTimeout(draw,500)
      });
    
  }.property("model","params")
})




//LIBRARY ROOT
App.LibraryRoute = Ember.Route.extend({
  activate: function() {
    var title = $(document).attr('title');
    $(document).attr('title', title+'-Library');
  },
  model:function(){
  },
  setupController: function(controller) {
    controller.set('title', "Library");
  }
});

App.LibraryIndexRoute = Ember.Route.extend({
  redirect : function(){
    this.transitionTo("library.all");
  }
});

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
    var libs = params.libs || dataURL.names;
    console.log(params.lib)
    if(libs=="woodruff"){
      var data = {
        title: 'Woodruff',
        student_info:[1,2,3]
      }
      dataURL.set('names', [data.title]);
      dataURL.set('paths', ["woodruff"]);
    }
    else if(libs=='health-science'){
      var data = {
        title: 'Health Science',
        student_info:[1,2,3]
      }
      dataURL.set('names', [data.title]);
      dataURL.set('paths', ["health-science"]);
    }
    else if(libs=='law'){
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
    // console.log(date);
  },
  afterModel: function (model){
    _this = this;
    var library_name = getLibName(_this.get('router.url'));
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


//Options Date Range
App.OptionalCalendarDatePicker = Ember.TextField.extend({
  _picker: null,
  
  modelChangedValue: function(){
    // console.log('inside OptionalCalendarDatePicker'+this.get("value"))
  }.observes("value"),
  
  didInsertElement: function(){
    var today = new Date(),
    yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);
    
    var start_date = dataURL.get('start') ||yesterday,
    end_date = dataURL.get('end') || today;
    
    $(".options-date-range .form-group>input")
    .datepicker({
      beforeShow: function(i,obj) {
        $widget = obj.dpDiv;
        window.$uiDatepickerDiv = $widget;
        $uiDatepickerDiv.addClass("ll-skin-melon").addClass("report-dates");
        if ($widget.data("top")) {
          setTimeout(function() {
            $uiDatepickerDiv.css( "top", $uiDatepickerDiv.data("top") );
          },50);
        }
      },
      maxDate: today,
      yearRange: '1999:c',
      dateFormat: "m/d/yy",
      onClose: function(i,obj) {
        $widget = obj.dpDiv;
        $widget.data("top", $widget.position().top);
      }
    });
    $(".options-date-range .form-group>input.start")
    .datepicker("setDate", start_date)
    
    $(".options-date-range .form-group>input.end")
    .datepicker("setDate", end_date)
  }
});

App.ClearFiltersButtonComponent = Ember.Component.extend({
  didInsertElement:function(){
    Ember.run.once(this,function(){
      Ember.run.next(this, function(){ 
        $("#clear-filters").on("click",function(evt){
          evt.preventDefault();
          
          var lib = dataURL.get('names');
          
          if(lib.length>1){
            lib = "all"
          }
          else{
            lib = lib[0].toLowerCase().replace(" ","-");
          }
          
          dataURL.set('category',null),
          dataURL.set('group',null)
          
          link = "#/library/"+lib;
          window.location = link;
        })
      });
    });
  }
})

App.ReloadChartDataButtonComponent = Ember.Component.extend({
  didInsertElement:function(){
    Ember.run.once(this,function(){
      $(".options-date-range .reload").on("click",function(evt){
        evt.preventDefault();
        var start = $(".options-date-range .form-group>input.start").datepicker("getDate");
        end = $(".options-date-range .form-group>input.end").datepicker("getDate");
        dataURL.set("start",start)
        dataURL.set("end",end)
        
        if($("#container-lastweek").length>0 && $(".mp-pushed").length>0){
          $(".loading-data.page-level").show();
          SUPERCHART();
        }
      })
    });
  }
})

App.DistinctUsersSwitchComponent = Ember.Component.extend({
  modelChangedValue: function(){
    // console.log('Distinct: '+this.get("value"))
    dataURL.set('distinct',this.get("value"));
    if($("#container-lastweek").length>0 && $(".mp-pushed").length>0){
      $(".loading-data.page-level").show();
      SUPERCHART();
    }
  }.observes("value"),
  didInsertElement:function(){
    this.set("value",dataURL.get('distinct'))
  }
})

App.OnOffCampusSwitchComponent = Ember.Component.extend({
  didInsertElement:function(){
    
    Ember.run.once(this,function(){
      Ember.run.next(this, function(){ 
        $('.options-campus .switch input').on("click",function(evt){
          var $this = $(this),
          val = $this.val();
          
          var current = dataURL.get("campus");
          if(current==val){
            $this.prop("checked", false);
            dataURL.set("campus",null);
          }
          else{
            dataURL.set("campus",val);
          }
          if($("#container-lastweek").length>0 && $(".mp-pushed").length>0){
            $(".loading-data.page-level").show();
            SUPERCHART();
          }
        });
      })
    })
    
  }
})



var selection = []

function formatDate(date){
  var formatted_date = (date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate())
  return formatted_date;
}

// function that builds both the charts on the Library pages
function SUPERCHART(){
  if(dataURL.get("drawing")){
    return
  }
  dataURL.set("drawing",true)
  
  var path = dataURL.get('paths'),
  d = '',
  uri_category = dataURL.get('category') || 'total_usage',
  uri_users = dataURL.get('group') || '';
  
  uri_category+='/';
  
  if(uri_users[0] && uri_users[0].length>0){
    uri_users=encodeURI(uri_users[0]);
    uri_users='/'+uri_users;
  }
  
  var $container = $('#container'),
  seriesOptions = [],
  yAxisOptions = [],
  seriesCounter = 0,
  enableLegend =false,
  names = dataURL.get('names'),
  colors= ['#FB715E','#7994FF','#5AA689','#FFD340','#796499'],
  uri_path = '/',
  start_date = dataURL.get('start'),
  end_date = dataURL.get('end'),
  date_range = '/'+formatDate(start_date)+'/'+formatDate(end_date)+'/',
  campus_tag = dataURL.get('campus') || '',
  distinct = dataURL.get('distinct') || false,
  distinct_tag = "";
  
  if(campus_tag!='' && campus_tag[0].length>0 ){
    campus_tag="/"+campus_tag[0];
    uri_category="on_off_campus/";
  }
  
  if(distinct){
    distinct_tag = "?distinct=True";
  }
  
  $.each(names, function(i, name) {
    var requestURL = uri_path+uri_category+path[i]+uri_users+campus_tag+date_range+distinct_tag;
    
    // console.log(requestURL);
    
    var json = $.getJSON(requestURL)
    
    json.done(function(data){
      if(data.data.length>0){
        jsonResponse(data)
      }
      else {
        data.data.push([(new Date).getTime(),0]);
        console.log(data.meta.library+" is empty.")
        jsonResponse(data)
      }
    })
    
    json.fail(function(){
      console.log('Error: JSON Ajax function failed.')
      var $error = $('<div/>').attr({'class':'error-loading'}).append('<span/>').html("<p>Sorry, the data failed to load from the server.</p>");
      $container.html($error);
      $error.fadeOut(0).fadeIn(500);
      dataURL.set("drawing","")
    });
    
    function jsonResponse(data) {
      d = data;
      if(data.data !== undefined){
        d = data.data;
      }
      else{
        d = data;
      }
      
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
        // console.log(seriesCounter)
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
        $(".loading-data.page-level").hide();
        dataURL.set("drawing",false)
      }
    }
    
    function drawChartLastWeek(data){
      var $container = $('#container-lastweek'),
      enableLegend = (data.length > 1 ? true : false);
      Highcharts.setOptions({
        global: {
          useUTC: false
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
        navigation: {
            buttonOptions: {
                theme: {
                    'stroke-width': 0,
                    stroke: "#DCDEE5",
                    r: 3,
                    style:{
                      'cursor':"pointer"
                    },
                    states: {
                        hover: {
                            fill: '#DCDEE5'
                        },
                        select: {
                            stroke: '#DCDEE5',
                            fill: '#DCDEE5'
                        }
                    }
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
          if(chart && chart.options.chart){
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
              ,maxDate:new Date
              ,onClose: function(i,obj) {
                $widget = obj.dpDiv;
                $widget.data("top", $widget.position().top);
              }
            })
          }
        },0)
      });//end highcharts
    }//end drawChartLastWeek
    
    function drawChart(data){
      var $container= $('#container'),
      enableLegend = (data.length > 1 ? true : false);
      Highcharts.setOptions({
        global: {
          useUTC: false
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
          selected: 6,
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
        navigation: {
            buttonOptions: {
                theme: {
                    'stroke-width': 0,
                    stroke: "#DCDEE5",
                    r: 3,
                    style:{
                      'cursor':"pointer"
                    },
                    states: {
                        hover: {
                            fill: '#DCDEE5'
                        },
                        select: {
                            stroke: '#DCDEE5',
                            fill: '#DCDEE5'
                        }
                    }
                }
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
              $uiDatepickerDiv.addClass("ll-skin-melon").removeClass("report-dates")
              if ($widget.data("top")) {
                setTimeout(function() {
                  $uiDatepickerDiv.css( "top", $uiDatepickerDiv.data("top") );
                },50);
              }
            },
            minDate: new Date(dataURL.get('start')),
            maxDate: new Date(dataURL.get('end')),
            onClose: function(i,obj) {
              $widget = obj.dpDiv;
              $widget.data("top", $widget.position().top);
            },
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
        SUPERCHART();
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
    $(".global-loading#onLoad").hide();
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
