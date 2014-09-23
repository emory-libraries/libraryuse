Highcharts.theme = {
  colors: [ "#0292EF","#24A1F2","#5DB7F2","#9AD1F5",
            "#3BC553","#5AD76F","#81E793","#B2F4BD",
            "#FF594C","#FF756B","#FF978F","#FFBFBA",
            "#FFBE4C","#FFC96B","#FFD68F","#FFE6BA",
            "#6E3FAF","#8A5EC8","#AA84DE","#CEB5F0"],
  chart: {
    borderWidth: 0,
    plotShadow: false,
    plotBackgroundColor: "transparent",
    plotBorderWidth: 0,
  },
  plotOptions: {
    pie: {
      borderWidth: 0
    }
  },
  title: {
    style: {
      color: '#3E576F',
      font: '16px "Open Sans", Arial, Helvetica, sans-serif'
    }
  },
  subtitle: {
    style: {
      color: '#6D869F',
      font: '12px "Open Sans", Arial, Helvetica, sans-serif'
    }
  },
  navigator: {
    outlineColor: 'transparent',
    height: 30
  },
  xAxis: {
    gridLineWidth: 0,
    lineColor: '#C0D0E0',
    tickColor: '#C0D0E0',
    labels: {
      style: {
        color: '#666',
        fontWeight: 'bold'
      }
    },
    title: {
      style: {
        color: '#666',
        font: '12px "Open Sans", Arial, Helvetica, sans-serif'
      }
    }
  },
  yAxis: {
    // alternateGridColor: 'rgba(255, 255, 255, .5)',
    lineColor: '#C0D0E0',
    tickColor: '#C0D0E0',
    tickWidth: 1,
    labels: {
      style: {
        color: '#666',
        fontWeight: 'bold'
      }
    },
    title: {
      style: {
        color: '#666',
        font: '12px "Open Sans", Arial, Helvetica, sans-serif'
      }
    }
  },
  legend: {
    itemStyle: {
      font: '9pt "Open Sans", Arial, Helvetica, sans-serif',
      color: '#3E576F'
    },
    itemHoverStyle: {
      color: 'black'
    },
    itemHiddenStyle: {
      color: 'silver'
    }
  },
  labels: {
    style: {
      color: '#3E576F'
    }
  },
  credits: false
};

// Apply the theme
var highchartsOptions = Highcharts.setOptions(Highcharts.theme);
