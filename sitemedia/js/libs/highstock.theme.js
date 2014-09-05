Highcharts.theme = {
  colors: ["#9AC3DB", "#FFDBAE", "#FFB4AE", "#9EE8AB", "#9CC6DF", "#FFDAAD", "#FFB3AD", "#9FEBAC", 
  "#B5D7EB", "#FFE3C0", "#FFC5C0", "#B7F2C1", "#CDE6F4", "#FFEBD3", "#FFD6D3", "#CDF8D5"],
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
  }
};

// Apply the theme
var highchartsOptions = Highcharts.setOptions(Highcharts.theme);
