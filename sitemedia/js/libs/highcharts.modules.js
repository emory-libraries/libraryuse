/**
 * Highcharts Drilldown module
 */
(function(g){function t(a,b,d){return"rgba("+[Math.round(a[0]+(b[0]-a[0])*d),Math.round(a[1]+(b[1]-a[1])*d),Math.round(a[2]+(b[2]-a[2])*d),a[3]+(b[3]-a[3])*d].join(",")+")"}var u=function(){},o=g.getOptions(),i=g.each,p=g.extend,z=g.format,A=g.pick,q=g.wrap,l=g.Chart,n=g.seriesTypes,v=n.pie,m=n.column,w=HighchartsAdapter.fireEvent,x=HighchartsAdapter.inArray,r=[];p(o.lang,{drillUpText:"â— Back to {series.name}"});o.drilldown={activeAxisLabelStyle:{cursor:"pointer",color:"#0d233a",fontWeight:"bold",
textDecoration:"underline"},activeDataLabelStyle:{cursor:"pointer",color:"#0d233a",fontWeight:"bold",textDecoration:"underline"},animation:{duration:500},drillUpButton:{position:{align:"right",x:-10,y:10}}};g.SVGRenderer.prototype.Element.prototype.fadeIn=function(a){this.attr({opacity:0.1,visibility:"inherit"}).animate({opacity:A(this.newOpacity,1)},a||{duration:250})};l.prototype.addSeriesAsDrilldown=function(a,b){this.addSingleSeriesAsDrilldown(a,b);this.applyDrilldown()};l.prototype.addSingleSeriesAsDrilldown=
function(a,b){var d=a.series,c=d.xAxis,f=d.yAxis,h;h=a.color||d.color;var e,y=[],g=[],k;k=d.levelNumber||0;b=p({color:h},b);e=x(a,d.points);i(d.chart.series,function(a){if(a.xAxis===c)y.push(a),g.push(a.userOptions),a.levelNumber=a.levelNumber||k});h={levelNumber:k,seriesOptions:d.userOptions,levelSeriesOptions:g,levelSeries:y,shapeArgs:a.shapeArgs,bBox:a.graphic.getBBox(),color:h,lowerSeriesOptions:b,pointOptions:d.options.data[e],pointIndex:e,oldExtremes:{xMin:c&&c.userMin,xMax:c&&c.userMax,yMin:f&&
f.userMin,yMax:f&&f.userMax}};if(!this.drilldownLevels)this.drilldownLevels=[];this.drilldownLevels.push(h);h=h.lowerSeries=this.addSeries(b,!1);h.levelNumber=k+1;if(c)c.oldPos=c.pos,c.userMin=c.userMax=null,f.userMin=f.userMax=null;if(d.type===h.type)h.animate=h.animateDrilldown||u,h.options.animation=!0};l.prototype.applyDrilldown=function(){var a=this.drilldownLevels,b;if(a&&a.length>0)b=a[a.length-1].levelNumber,i(this.drilldownLevels,function(a){a.levelNumber===b&&i(a.levelSeries,function(a){a.levelNumber===
b&&a.remove(!1)})});this.redraw();this.showDrillUpButton()};l.prototype.getDrilldownBackText=function(){var a=this.drilldownLevels;if(a&&a.length>0)return a=a[a.length-1],a.series=a.seriesOptions,z(this.options.lang.drillUpText,a)};l.prototype.showDrillUpButton=function(){var a=this,b=this.getDrilldownBackText(),d=a.options.drilldown.drillUpButton,c,f;this.drillUpButton?this.drillUpButton.attr({text:b}).align():(f=(c=d.theme)&&c.states,this.drillUpButton=this.renderer.button(b,null,null,function(){a.drillUp()},
c,f&&f.hover,f&&f.select).attr({align:d.position.align,zIndex:9}).add().align(d.position,!1,d.relativeTo||"plotBox"))};l.prototype.drillUp=function(){for(var a=this,b=a.drilldownLevels,d=b[b.length-1].levelNumber,c=b.length,f=a.series,h=f.length,e,g,j,k,l=function(b){var c;i(f,function(a){a.userOptions===b&&(c=a)});c=c||a.addSeries(b,!1);if(c.type===g.type&&c.animateDrillupTo)c.animate=c.animateDrillupTo;b===e.seriesOptions&&(j=c)};c--;)if(e=b[c],e.levelNumber===d){b.pop();g=e.lowerSeries;if(!g.chart)for(;h--;)if(f[h].options.id===
e.lowerSeriesOptions.id){g=f[h];break}g.xData=[];i(e.levelSeriesOptions,l);w(a,"drillup",{seriesOptions:e.seriesOptions});if(j.type===g.type)j.drilldownLevel=e,j.options.animation=a.options.drilldown.animation,g.animateDrillupFrom&&g.animateDrillupFrom(e);j.levelNumber=d;g.remove(!1);if(j.xAxis)k=e.oldExtremes,j.xAxis.setExtremes(k.xMin,k.xMax,!1),j.yAxis.setExtremes(k.yMin,k.yMax,!1)}this.redraw();this.drilldownLevels.length===0?this.drillUpButton=this.drillUpButton.destroy():this.drillUpButton.attr({text:this.getDrilldownBackText()}).align();
r.length=[]};m.prototype.supportsDrilldown=!0;m.prototype.animateDrillupTo=function(a){if(!a){var b=this,d=b.drilldownLevel;i(this.points,function(a){a.graphic.hide();a.dataLabel&&a.dataLabel.hide();a.connector&&a.connector.hide()});setTimeout(function(){i(b.points,function(a,b){var h=b===(d&&d.pointIndex)?"show":"fadeIn",e=h==="show"?!0:void 0;a.graphic[h](e);if(a.dataLabel)a.dataLabel[h](e);if(a.connector)a.connector[h](e)})},Math.max(this.chart.options.drilldown.animation.duration-50,0));this.animate=
u}};m.prototype.animateDrilldown=function(a){var b=this,d=this.chart.drilldownLevels,c=this.chart.drilldownLevels[this.chart.drilldownLevels.length-1].shapeArgs,f=this.chart.options.drilldown.animation;if(!a)i(d,function(a){if(b.userOptions===a.lowerSeriesOptions)c=a.shapeArgs}),c.x+=this.xAxis.oldPos-this.xAxis.pos,i(this.points,function(a){a.graphic&&a.graphic.attr(c).animate(a.shapeArgs,f);a.dataLabel&&a.dataLabel.fadeIn(f)}),this.animate=null};m.prototype.animateDrillupFrom=function(a){var b=
this.chart.options.drilldown.animation,d=this.group,c=this;i(c.trackerGroups,function(a){if(c[a])c[a].on("mouseover")});delete this.group;i(this.points,function(c){var h=c.graphic,e=g.Color(c.color).rgba,i=g.Color(a.color).rgba,j=function(){h.destroy();d&&(d=d.destroy())};h&&(delete c.graphic,b?h.animate(a.shapeArgs,g.merge(b,{step:function(a,b){b.prop==="start"&&e.length===4&&i.length===4&&this.attr({fill:t(e,i,b.pos)})},complete:j})):(h.attr(a.shapeArgs),j()))})};v&&p(v.prototype,{supportsDrilldown:!0,
animateDrillupTo:m.prototype.animateDrillupTo,animateDrillupFrom:m.prototype.animateDrillupFrom,animateDrilldown:function(a){var b=this.chart.drilldownLevels[this.chart.drilldownLevels.length-1],d=this.chart.options.drilldown.animation,c=b.shapeArgs,f=c.start,h=(c.end-f)/this.points.length,e=g.Color(b.color).rgba;if(!a)i(this.points,function(a,b){var i=g.Color(a.color).rgba;a.graphic.attr(g.merge(c,{start:f+b*h,end:f+(b+1)*h}))[d?"animate":"attr"](a.shapeArgs,g.merge(d,{step:function(a,b){b.prop===
"start"&&e.length===4&&i.length===4&&this.attr({fill:t(e,i,b.pos)})}}))}),this.animate=null}});g.Point.prototype.doDrilldown=function(a){for(var b=this.series.chart,d=b.options.drilldown,c=(d.series||[]).length,f;c--&&!f;)d.series[c].id===this.drilldown&&x(this.drilldown,r)===-1&&(f=d.series[c],r.push(this.drilldown));w(b,"drilldown",{point:this,seriesOptions:f});f&&(a?b.addSingleSeriesAsDrilldown(this,f):b.addSeriesAsDrilldown(this,f))};q(g.Point.prototype,"init",function(a,b,d,c){var f=a.call(this,
b,d,c),h=b.chart,e=(a=b.xAxis&&b.xAxis.ticks[c])&&a.label;if(f.drilldown){if(g.addEvent(f,"click",function(){f.doDrilldown()}),e){if(!e.basicStyles)e.basicStyles=g.merge(e.styles);e.addClass("highcharts-drilldown-axis-label").css(h.options.drilldown.activeAxisLabelStyle).on("click",function(){i(e.ddPoints,function(a){a.doDrilldown&&a.doDrilldown(!0)});h.applyDrilldown()});if(!e.ddPoints)e.ddPoints=[];e.ddPoints.push(f)}}else if(e&&e.basicStyles)e.styles={},e.css(e.basicStyles);return f});q(g.Series.prototype,
"drawDataLabels",function(a){var b=this.chart.options.drilldown.activeDataLabelStyle;a.call(this);i(this.points,function(a){if(a.drilldown&&a.dataLabel)a.dataLabel.attr({"class":"highcharts-drilldown-data-label"}).css(b).on("click",function(){a.doDrilldown()})})});var s,o=function(a){a.call(this);i(this.points,function(a){a.drilldown&&a.graphic&&a.graphic.attr({"class":"highcharts-drilldown-point"}).css({cursor:"pointer"})})};for(s in n)n[s].prototype.supportsDrilldown&&q(n[s].prototype,"drawTracker",
o)})(Highcharts);


/*
 Highcharts JS v4.0.4 (2014-09-02)
 Exporting module

 (c) 2010-2014 Torstein Honsi

 License: www.highcharts.com/license
*/
(function(f){var A=f.Chart,t=f.addEvent,B=f.removeEvent,l=f.createElement,o=f.discardElement,v=f.css,k=f.merge,r=f.each,p=f.extend,D=Math.max,j=document,C=window,E=f.isTouchDevice,F=f.Renderer.prototype.symbols,s=f.getOptions(),y;p(s.lang,{printChart:"Print chart",downloadPNG:"Download PNG image",downloadJPEG:"Download JPEG image",downloadPDF:"Download PDF document",downloadSVG:"Download SVG vector image",contextButtonTitle:"Chart context menu"});s.navigation={menuStyle:{border:"1px solid #A0A0A0",
background:"#FFFFFF",padding:"5px 0"},menuItemStyle:{padding:"0 10px",background:"none",color:"#303030",fontSize:E?"14px":"11px"},menuItemHoverStyle:{background:"#4572A5",color:"#FFFFFF"},buttonOptions:{symbolFill:"#E0E0E0",symbolSize:14,symbolStroke:"#666",symbolStrokeWidth:3,symbolX:12.5,symbolY:10.5,align:"right",buttonSpacing:3,height:22,theme:{fill:"white",stroke:"none"},verticalAlign:"top",width:24}};s.exporting={type:"image/png",url:"http://export.highcharts.com/",buttons:{contextButton:{menuClassName:"highcharts-contextmenu",
symbol:"menu",_titleKey:"contextButtonTitle",menuItems:[{textKey:"printChart",onclick:function(){this.print()}},{separator:!0},{textKey:"downloadPNG",onclick:function(){this.exportChart()}},{textKey:"downloadJPEG",onclick:function(){this.exportChart({type:"image/jpeg"})}},{textKey:"downloadPDF",onclick:function(){this.exportChart({type:"application/pdf"})}},{textKey:"downloadSVG",onclick:function(){this.exportChart({type:"image/svg+xml"})}}]}}};f.post=function(b,a,d){var c,b=l("form",k({method:"post",
action:b,enctype:"multipart/form-data"},d),{display:"none"},j.body);for(c in a)l("input",{type:"hidden",name:c,value:a[c]},null,b);b.submit();o(b)};p(A.prototype,{getSVG:function(b){var a=this,d,c,z,h,g=k(a.options,b);if(!j.createElementNS)j.createElementNS=function(a,b){return j.createElement(b)};b=l("div",null,{position:"absolute",top:"-9999em",width:a.chartWidth+"px",height:a.chartHeight+"px"},j.body);c=a.renderTo.style.width;h=a.renderTo.style.height;c=g.exporting.sourceWidth||g.chart.width||
/px$/.test(c)&&parseInt(c,10)||600;h=g.exporting.sourceHeight||g.chart.height||/px$/.test(h)&&parseInt(h,10)||400;p(g.chart,{animation:!1,renderTo:b,forExport:!0,width:c,height:h});g.exporting.enabled=!1;g.series=[];r(a.series,function(a){z=k(a.options,{animation:!1,enableMouseTracking:!1,showCheckbox:!1,visible:a.visible});z.isInternal||g.series.push(z)});d=new f.Chart(g,a.callback);r(["xAxis","yAxis"],function(b){r(a[b],function(a,c){var g=d[b][c],f=a.getExtremes(),h=f.userMin,f=f.userMax;g&&(h!==
void 0||f!==void 0)&&g.setExtremes(h,f,!0,!1)})});c=d.container.innerHTML;g=null;d.destroy();o(b);c=c.replace(/zIndex="[^"]+"/g,"").replace(/isShadow="[^"]+"/g,"").replace(/symbolName="[^"]+"/g,"").replace(/jQuery[0-9]+="[^"]+"/g,"").replace(/url\([^#]+#/g,"url(#").replace(/<svg /,'<svg xmlns:xlink="http://www.w3.org/1999/xlink" ').replace(/ href=/g," xlink:href=").replace(/\n/," ").replace(/<\/svg>.*?$/,"</svg>").replace(/(fill|stroke)="rgba\(([ 0-9]+,[ 0-9]+,[ 0-9]+),([ 0-9\.]+)\)"/g,'$1="rgb($2)" $1-opacity="$3"').replace(/&nbsp;/g,
"Â ").replace(/&shy;/g,"Â­").replace(/<IMG /g,"<image ").replace(/height=([^" ]+)/g,'height="$1"').replace(/width=([^" ]+)/g,'width="$1"').replace(/hc-svg-href="([^"]+)">/g,'xlink:href="$1"/>').replace(/id=([^" >]+)/g,'id="$1"').replace(/class=([^" >]+)/g,'class="$1"').replace(/ transform /g," ").replace(/:(path|rect)/g,"$1").replace(/style="([^"]+)"/g,function(a){return a.toLowerCase()});return c=c.replace(/(url\(#highcharts-[0-9]+)&quot;/g,"$1").replace(/&quot;/g,"'")},exportChart:function(b,a){var b=
b||{},d=this.options.exporting,d=this.getSVG(k({chart:{borderRadius:0}},d.chartOptions,a,{exporting:{sourceWidth:b.sourceWidth||d.sourceWidth,sourceHeight:b.sourceHeight||d.sourceHeight}})),b=k(this.options.exporting,b);f.post(b.url,{filename:b.filename||"chart",type:b.type,width:b.width||0,scale:b.scale||2,svg:d},b.formAttributes)},print:function(){var b=this,a=b.container,d=[],c=a.parentNode,f=j.body,h=f.childNodes;if(!b.isPrinting)b.isPrinting=!0,r(h,function(a,b){if(a.nodeType===1)d[b]=a.style.display,
a.style.display="none"}),f.appendChild(a),C.focus(),C.print(),setTimeout(function(){c.appendChild(a);r(h,function(a,b){if(a.nodeType===1)a.style.display=d[b]});b.isPrinting=!1},1E3)},contextMenu:function(b,a,d,c,f,h,g){var e=this,k=e.options.navigation,q=k.menuItemStyle,m=e.chartWidth,n=e.chartHeight,j="cache-"+b,i=e[j],u=D(f,h),w,x,o,s=function(a){e.pointer.inClass(a.target,b)||x()};if(!i)e[j]=i=l("div",{className:b},{position:"absolute",zIndex:1E3,padding:u+"px"},e.container),w=l("div",null,p({MozBoxShadow:"3px 3px 10px #888",
WebkitBoxShadow:"3px 3px 10px #888",boxShadow:"3px 3px 10px #888"},k.menuStyle),i),x=function(){v(i,{display:"none"});g&&g.setState(0);e.openMenu=!1},t(i,"mouseleave",function(){o=setTimeout(x,500)}),t(i,"mouseenter",function(){clearTimeout(o)}),t(document,"mouseup",s),t(e,"destroy",function(){B(document,"mouseup",s)}),r(a,function(a){if(a){var b=a.separator?l("hr",null,null,w):l("div",{onmouseover:function(){v(this,k.menuItemHoverStyle)},onmouseout:function(){v(this,q)},onclick:function(){x();a.onclick.apply(e,
arguments)},innerHTML:a.text||e.options.lang[a.textKey]},p({cursor:"pointer"},q),w);e.exportDivElements.push(b)}}),e.exportDivElements.push(w,i),e.exportMenuWidth=i.offsetWidth,e.exportMenuHeight=i.offsetHeight;a={display:"block"};d+e.exportMenuWidth>m?a.right=m-d-f-u+"px":a.left=d-u+"px";c+h+e.exportMenuHeight>n&&g.alignOptions.verticalAlign!=="top"?a.bottom=n-c-u+"px":a.top=c+h-u+"px";v(i,a);e.openMenu=!0},addButton:function(b){var a=this,d=a.renderer,c=k(a.options.navigation.buttonOptions,b),j=
c.onclick,h=c.menuItems,g,e,l={stroke:c.symbolStroke,fill:c.symbolFill},q=c.symbolSize||12;if(!a.btnCount)a.btnCount=0;if(!a.exportDivElements)a.exportDivElements=[],a.exportSVGElements=[];if(c.enabled!==!1){var m=c.theme,n=m.states,o=n&&n.hover,n=n&&n.select,i;delete m.states;j?i=function(){j.apply(a,arguments)}:h&&(i=function(){a.contextMenu(e.menuClassName,h,e.translateX,e.translateY,e.width,e.height,e);e.setState(2)});c.text&&c.symbol?m.paddingLeft=f.pick(m.paddingLeft,25):c.text||p(m,{width:c.width,
height:c.height,padding:0});e=d.button(c.text,0,0,i,m,o,n).attr({title:a.options.lang[c._titleKey],"stroke-linecap":"round"});e.menuClassName=b.menuClassName||"highcharts-menu-"+a.btnCount++;c.symbol&&(g=d.symbol(c.symbol,c.symbolX-q/2,c.symbolY-q/2,q,q).attr(p(l,{"stroke-width":c.symbolStrokeWidth||1,zIndex:1})).add(e));e.add().align(p(c,{width:e.width,x:f.pick(c.x,y)}),!0,"spacingBox");y+=(e.width+c.buttonSpacing)*(c.align==="right"?-1:1);a.exportSVGElements.push(e,g)}},destroyExport:function(b){var b=
b.target,a,d;for(a=0;a<b.exportSVGElements.length;a++)if(d=b.exportSVGElements[a])d.onclick=d.ontouchstart=null,b.exportSVGElements[a]=d.destroy();for(a=0;a<b.exportDivElements.length;a++)d=b.exportDivElements[a],B(d,"mouseleave"),b.exportDivElements[a]=d.onmouseout=d.onmouseover=d.ontouchstart=d.onclick=null,o(d)}});F.menu=function(b,a,d,c){return["M",b,a+2.5,"L",b+d,a+2.5,"M",b,a+c/2+0.5,"L",b+d,a+c/2+0.5,"M",b,a+c-1.5,"L",b+d,a+c-1.5]};A.prototype.callbacks.push(function(b){var a,d=b.options.exporting,
c=d.buttons;y=0;if(d.enabled!==!1){for(a in c)b.addButton(c[a]);t(b,"destroy",b.destroyExport)}})})(Highcharts);


/**
 * A small plugin for getting the CSV of a categorized chart
 */
/*global Highcharts, document */
(function (Highcharts) {

    'use strict';

    var each = Highcharts.each,
        downloadAttrSupported = document.createElement('a').download !== undefined;


    Highcharts.Chart.prototype.getCSV = function () {
        var columns = [],
            line,
            csv = '',
            row,
            col,
            maxRows,
            options = (this.options.exporting || {}).csv || {},

            // Options
            dateFormat = options.dateFormat || '%Y-%m-%d %H:%M:%S',
            itemDelimiter = options.itemDelimiter || ';', // use ';' for direct import to Excel
            lineDelimiter = (downloadAttrSupported ? options.lineDelimiter || '%0A' : options.lineDelimiter || '\n\r'); // '\n' isn't working with the js csv data extraction


        each(this.series, function (series) {
            if (series.options.includeInCSVExport !== false) {
                if (series.xAxis) {
                    var xData = series.xData.slice(),
                        xTitle = 'X values';
                    if (series.xAxis.isDatetimeAxis) {
                        xData = Highcharts.map(xData, function (x) {
                            return Highcharts.dateFormat(dateFormat, x);
                        });
                        xTitle = 'DateTime';
                    } else if (series.xAxis.categories) {
                        xData = Highcharts.map(xData, function (x) {
                            return Highcharts.pick(series.xAxis.categories[x], x);
                        });
                        xTitle = 'Category';
                    }
                    columns.push(xData);
                    columns[columns.length - 1].unshift(xTitle);
                }
                columns.push(series.yData.slice());
                columns[columns.length - 1].unshift(series.name);
            }
        });

        // Transform the columns to CSV
        maxRows = Math.max.apply(this, Highcharts.map(columns, function (col) { return col.length; }));
        for (row = 0; row < maxRows; row = row + 1) {
            line = [];
            for (col = 0; col < columns.length; col = col + 1) {
                line.push(columns[col][row]);
            }
            csv += line.join(itemDelimiter) + lineDelimiter;
        }

        return csv;
    };

    // Add "Download CSV" to the exporting menu. Use download attribute if supported, else
    // run a simple PHP script that returns a file. The source code for the PHP script can be viewed at
    // https://raw.github.com/highslide-software/highcharts.com/master/studies/csv-export/csv.php
    if (Highcharts.getOptions().exporting) {
        Highcharts.getOptions().exporting.buttons.contextButton.menuItems.push({
            text: Highcharts.getOptions().lang.downloadCSV || 'Download CSV',
            onclick: function () {
                var a;

                // Download attribute supported
                if (downloadAttrSupported) {
                    // Client side extraction
                    a = document.createElement('a');
                    a.href        = 'data:attachment/csv,' + this.getCSV();
                    a.target      = '_blank';
                    a.download    = (this.title ? this.title.textStr.replace(/ /g, '-').toLowerCase() : 'chart') + '.csv';
                    document.body.appendChild(a);
                    a.click();
                    a.remove();

                // Fall back to server side handling
                } else {
                    Highcharts.post('http://www.highcharts.com/studies/csv-export/csv.php', {
                        csv: this.getCSV()
                    });
                }

            }
        });
    }
}(Highcharts));
