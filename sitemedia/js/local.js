$(document).ready(function(){
  $(document).on('click','.tab-pane .nav-pills>li',function(){
    var $this = $(this);
  })
  .on('click','.nav-toggle>li>a',function(){
    var $this = $(this),
        $parentLI = $this.parent('li'),
        $parentLI_active = $this.parent('li');

    $parentLI_active.removeClass('active');

    if($parentLI.hasClass('value-set')){
      $parentLI.removeClass('value-set').removeClass('active');
    }
    else{
      $parentLI.addClass('value-set').addClass('active');
    }
    var selectedCount = $parentLI.parent('ul').children('li.value-set').length,
        $topLevelTabs = $('.tab-pane.active>.tab-content .nav>li.active, #filterTabs>.nav>li.active');

    console.log(selectedCount);
    if(selectedCount>0){
      $topLevelTabs.addClass('value-set');
    }
    else{
      $topLevelTabs.removeClass('value-set');
    }

  })

  .on('click', '.submenu #global-options li>a', function(evt){
    evt.preventDefault();
    var $this = $(this);
        $("#global-options .active").removeClass('active');
        $this.addClass('active');
  })
  .on('click','.highcharts-button',function(){
    console.log('need to add dates stuff')
  })

});//end doc.ready



