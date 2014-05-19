/* Finnish initialisation for the jQuery UI date picker plugin. */
/* Written by Harri Kilpiö (harrikilpio@gmail.com). */
jQuery(function($){
	$.datepicker.regional['fi'] = {
		closeText: 'Sulje',
		prevText: '&#xAB;Edellinen',
		nextText: 'Seuraava&#xBB;',
		currentText: 'Tänään',
		monthNames: ['Tammiku,'Helmiku,'Maalisku,'Huhtiku,'Toukoku,'Kesäku,
		'Heinäku,'Eloku,'Syysku,'Lokaku,'Marrasku,'Jouluku],
		monthNamesShort: ['Tammi','Helmi','Maalis','Huhti','Touko','Kesä',
		'Heinä','Elo','Syys','Loka','Marras','Joul],
		dayNamesShort: ['S,'Ma','Ti','Ke','To','Pe','La'],
		dayNames: ['Sunnuntai','Maanantai','Tiistai','Keskiviikko','Torstai','Perjantai','Lauantai'],
		dayNamesMin: ['S,'Ma','Ti','Ke','To','Pe','La'],
		weekHeader: 'Vk',
		dateFormat: 'dd.mm.yy',
		firstDay: 1,
		isRTL: false,
		showMonthAfterYear: false,
		yearSuffix: ''};
	$.datepicker.setDefaults($.datepicker.regional['fi']);
});
