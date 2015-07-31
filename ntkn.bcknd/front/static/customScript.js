$(function (){
		var getDeepLink = function(){
			"use strict";
			var paramaters = {}
			paramaters.de = $('#ap_origin_flight_hidden').val() || '';
			paramaters.a = $('#ap_dest_flight_hidden').val() || '';
			if ($('#ap-RoundTrip').is(':checked'))
				paramaters.tipoViaje = 'IV'
			else if($('#ap-OneWay').is(':checked'))
				paramaters.tipoViaje = 'I'
			else
				paramaters.tipoViaje = 'I' //Never sould pass here
			paramaters.ida = ($('#ap_flight_start_hidden').val() || '').replace(/\//g, '');
			paramaters.vuelta = ($('#ap_flight_end_hidden').val() || '').replace(/\//g, '');
			paramaters.adultos = $('#ap_booker_flight_adults1').val();
			paramaters.ninyos = $('#ap_booker_flight_minors1').val();
			paramaters.bebes = '0'; //We have no babies data
			paramaters.horaIda = '0000';
			paramaters.horaVuelta = '0000';
			paramaters.residente = 'N';
			paramaters.web_origen = ''
			paramaters.utm_source = ''
			paramaters.utm_medium = ''
			paramaters.utm_campaign = ''
			paramaters.utm_term = ''
			paramaters.utm_content = ''

			if (paramaters.de == '' || paramaters.a == '')
				return undefined;

			var veciUrlRoot = 'http://www.viajeselcorteingles.es/viajeseci/vuelos/view/flight/nuevaDisponibilidad.jsf?';
			var tdUrlRoot = 'http://clk.tradedoubler.com/click?p=12345&a=12345&g=12345&url=';
			var href = tdUrlRoot + veciUrlRoot + $.param(paramaters);
			var deeplink = $("<a>");
			deeplink.attr('href', href);
			deeplink.attr('target', '_blank');
			deeplink.html("Cotizar en una nueva venta: <input type='checkbox'></input>")
			return deeplink;
		};

		var checkingDeepLink = function (){
			if (getDeepLink() != undefined){
				var deepLinkTag = getDeepLink();
				console.log(deepLinkTag);
				deepLinkTag.insertBefore($("#ap_booker_Flight").find(".ptw-buttons"));
				clearInterval(checkingBoxes);
			}
		}
		var checkingBoxes = setInterval(checkingDeepLink, 100);
});
