  $(document).ready(function(){

  midatatable = $('#midatatable').DataTable({
        "lengthMenu": [
            [5, 25, 50, -1],
            [5, 25, 50, "All"]
        ],
        dom: 'Brtlip',
        buttons: [
            { extend: 'copy',
              text: 'Copiar',
              className: 'btn btn-warning'},
            { extend: 'excel',
              text: 'Excel',
              className: 'btn btn-success'},
            { text: 'PDF',
					    extend: 'pdfHtml5',
					    filename: 'Reporte_Pedidos',
					    orientation: 'portrait', //portrait
					    pageSize: 'A4', //A3 , A5 , A6 , legal , letter
					    exportOptions: {
    						columns: 'thead th:not(.noExport)',
    						search: 'applied',
    						order: 'applied'
					    },
              className: 'btn btn-danger',
					customize: function (doc) {
            var titulo = $('.titulo_reporte').val();
            var empresa = $('.empresa_reporte').val();
            var direccion = $('.direccion_reporte').val();
            var telefono = $('.telefono_reporte').val();
            var usuario = $('.usuario_reporte').val();
						//Remove the title created by datatTables
						// doc.content.splice(0,1);
            doc.content[0] = [{text: titulo + "\n", fontSize:15},{text:"", alignment:'left'}];

						//Create a date string that we use in the footer. Format is dd-mm-yyyy
						var now = new Date();
						var jsDate = now.getDate()+'/'+(now.getMonth()+1)+'/'+now.getFullYear();
						// Logo converted to base64
						// var logo = getBase64FromImageUrl('https://datatables.net/media/images/logo.png');
						// The above call should work, but not when called from codepen.io
						// So we use a online converter and paste the string in.
						// Done on http://codebeautify.org/image-to-base64-converter
						// It's a LONG string scroll down to see the rest of the code !!!
						var logo = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAL2AqoDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD3+iiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKA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M/5C1n/13T/0IV93WX/HjB/1zX+VAE9FFFABRRRQAUUUUAFFFFABVHWv+QDqP/XtJ/6CavVR1r/kA6j/ANe0n/oJoA+E7n/j6m/3z/Ooqluf+Pqb/fP86ioAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAtaZ/yFrP/run/oQr7usv+PGD/rmv8q+EdM/5C1n/ANd0/wDQhX3dZf8AHjB/1zX+VAE9FFFABRRRQAUUUUAFFFFABVHWv+QDqP8A17Sf+gmr1Uda/wCQDqP/AF7Sf+gmgD4Tuf8Aj6m/3z/Ooqluf+Pqb/fP86ioAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAtaZ/wAhaz/67p/6EK+7rL/jxg/65r/KvhLS/wDkLWX/AF3T/wBCFfdtmMWUAP8AzzX+VAE9FFFABRRRQAUUUUAFFFFABVHWv+QDqP8A17Sf+gmr1QXsP2iwuYP+ekTJ+YIoA+DLn/j6m/3z/Ooqu6xB9l1u/t8Y8q5kT8mIqlQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFORGkcIilmJwABkmu38PfCXxd4jVZIdNe3gP8Ay0uf3fHqAcE0AcNRX0Ho/wCzfCFVtZ1mQt1K2qgfh8wNdvYfBLwPZxhZtMN2w/jllcH/AMdIoA+RaK+1bf4beDrXHk6DajHqWb+ZrSTwn4eRdq6LY4H/AEwU/wBKAPhiivuj/hFtA/6A1h/34X/Cj/hFtA/6A1h/34X/AAoA+F6K+6P+EW0D/oDWH/fhf8KP+EW0D/oDWH/fhf8ACgD4Xor7o/4RbQP+gNYf9+F/wo/4RbQP+gNYf9+F/wAKAPheivuj/hFtA/6A1h/3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iiigAooooAKKKKACiiigAooooAKKKKACiiigDB8a/wDIl6v/ANe7V8PV9w+Nf+RL1f8A692r4eoAKKKKACiiigAooooAKKKKACvpL9nD/kWtU/6+v/ZVr5tr6S/Zw/5FrVP+vr/2VaAPbaKKKACiiigAooooAKKKKACiiigAooooAKKKKAPKP2gP+Sd/9vCfzFfK9fVH7QH/ACTv/t4T+Yr5XoAkhgluH2QxtI2M4UZNWP7Kv/8Anzn/AO+DXpf7PyK/xDkDqGH2OTgjPpX1J9ng/wCeMf8A3yKAPi/QPhz4o8R3KRWmlzpGSN00qFUUfWvqH4efD6x8CaP5MZE19KMzz4xk+g9q7JUVBhVCj2GKWgAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArzn44f8kr1H/rpF/6GK9GrlPiL4Zu/F/gy60aylijnldGVpSQvytnsDQB8V13/gP4W33jvT57u1vIoVhfYQ/euj/4Z08Uf9BDTP8Av4//AMTXrfwp8C6j4F0i7tNRnt5Xmk3KYGJGPxAoA8u/4Zz1nH/IUtv1rzDWfCWraL4kl0Sa2drlJPLUopIfnAI9q+4qry2NpNcx3MttE88f3JGUFl+hoAx/BGjyaD4M0vTphiaK3TzB6MQMj866CiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAMHxr/AMiXq/8A17tXw9X3D41/5EvV/wDr3avh6gAooooAKKKKACiiigAooooAK99/Zw1eJH1XSXcLI2JkBP3uxx+VeBVqeHdevPDOu2uq2LlZoHDYzww7g+xoA+66K5DwX8RND8ZWKPa3Kx3YA8y3k+Vgf6119ABRRRQAUUUUAFFFFABRRRQAUUUUAFFFc54q8b6H4QsGudSu1D4+SFDl3PoB/jQB5v8AtFarFD4bsNMDgzTylyo7AYwf518110PjPxXd+MfEdxql0zbWO2GMn7idh/X8a56gD1n9nv8A5KJJ/wBecn9K+pq+Wf2e/wDkokn/AF5yf0r6moAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiii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JJqGiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAPWf2e/+SiSf9ecn9K+pq+Wf2e/+SiSf9ecn9K+pqACiiigAooooA5b4j376Z8O9auo22sIQmf95gv/ALNXxSTk5NfYHxrJX4Q66QcH9x/6Pjr4/oAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA9Z/Z7/wCSiSf9ecn8xX1NXyz+z3/yUST/AK85P6V9TUAFFFFABRRRQB5/8bP+SQa7/wBu/wD6UR18gV9f/Gz/AJJBrv8A27/+lEdfIFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAHrP7Pf/JRJP8Arzk/pX1NXyz+z3/yUST/AK85P6V9TUAFFFFABRRRQB5/8bP+SQa7/wBu/wD6UR18gV9f/Gz/AJJBrv8A27/+lEdfIFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAHrP7Pf/JRJP8Arzk/pX1NXyz+z3/yUST/AK85P6V9TUAF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+GabP/oZ5/8AwDH/AMXQB870V9Ef8M02f/Qzz/8AgGP/AIuj/hmmz/6Gef8A8Ax/8XQB870V9Ef8M02f/Qzz/wDgGP8A4uj/AIZps/8AoZ5//AMf/F0AfO9FfRH/AAzTZ/8AQzz/APgGP/i6P+GabP8A6Gef/wAAx/8AF0AfO9FfRH/DNNn/ANDPP/4Bj/4uj/hmmz/6Gef/AMAx/wDF0AfO9FfRH/DNNn/0M8//AIBj/wCLo/4Zps/+hnn/APAMf/F0AfO9FfRH/DNNn/0M8/8A4Bj/AOLo/wCGabP/AKGef/wDH/xdAHzvRX0R/wAM02f/AEM8/wD4Bj/4uj/hmmz/AOhnn/8AAMf/ABdAHzvRX0R/wzTZ/wDQzz/+AY/+Lo/4Zps/+hnn/wDAMf8AxdAHzvRX0R/wzTZ/9DPP/wCAY/8Ai6P+GabP/oZ5/wDwDH/xdAHzvRX0R/wzTZ/9DPP/AOAY/wDi6P8Ahmmz/wChnn/8Ax/8XQB870V9Gwfs26YjZm8QXEo9BbBf/Zq6jRPgf4O0lhJNavfSDvcHK/8AfNAHzr4Q+H2u+MrxY7G1ZLbcBJcuCEQV9V+CPAul+B9JFrZJvuHAM07D5nP+FdJbWsFlbR21tEkUMYwiIMBR7CpaACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAP/Z';
						// A documentation reference can be found at
						// https://github.com/bpampuch/pdfmake#getting-started
						// Set page margins [left,top,right,bottom] or [horizontal,vertical]
						// or one number for equal spread
						// It's important to create enough space at the top for a header !!!
						doc.pageMargins = [50,160,0,50];
						// Set the font size fot the entire document
						doc.defaultStyle.fontSize = 9;
						// Set the fontsize for the table header
						doc.styles.tableHeader.fontSize = 9;
						// Create a header object with 3 columns
						// Left side: Logo
						// Middle: brandname
						// Right side: A document title
						doc['header']=(function() {
							return {
								columns: [
									{
										image: logo,
										width: 50
									},
                  {
										alignment: 'center',
										text:[{text: empresa + "\n \n ", bold:true, fontSize:12}, {text: direccion + "\n" + "Teléfono: " + telefono + "\n \n \n" }],
										fontSize: 10,
										margin: [0,20,0,0]
									},
									{
										alignment: 'right',
										fontSize: 9,
										text: ['Fecha: ', { text: jsDate.toString() }, {text: '\n Generado por: ' + usuario, fontSize:7}],
                    width:80,
										margin: [0,10,0,0],
                    alignment:'left'
									}
								],
								margin: 20
							}
						});

						// Create a footer object with 2 columns
						// Left side: report creation date
						// Right side: current page and total pages
						doc['footer']=(function(page, pages) {
							return {
								columns: [
									{
										alignment: 'left',
										text: ['Generado el: ', { text: jsDate.toString() }],
                    fontSize: 9,
									},
									{
										alignment: 'right',
										text: ['Página ', { text: page.toString() },	' de ',	{ text: pages.toString() }],
                    fontSize: 9,
									}
								],
								margin: 20
							}
						});
            //Funcion que pone cada columna en tamaño *, para que se ajuste automagicamente. cuenta cada <td> del data table y genera array del tipo [*,*,*,..,n] y establece dicho array como width.
                var colCount = new Array();
                $("#midatatable").find('tbody tr:first-child td').each(function() {
                    if ($(this).attr('colspan')) {
                        for (var j = 1; j <= $(this).attr('colspan'); $j++) {
                            colCount.push('*');
                        }
                    } else { colCount.push('*'); }
                });
                //console.log(colCount);
                // colCount.push('*'); //Le pongo uno mas porque tengo un td oculto (el id)
                doc.content[1].table.widths = colCount;
                var table = $("#midatatable").DataTable();//Obtengo la tabla
                var pageInfo = table.page.info(); //Obtiene el objeto page.info()
                for (i = 1; i <= pageInfo.recordsDisplay; i++) { //recordsDisplay me devuelve la cantidad de registros mostrados
                  doc.content[1].table.body[i][5].alignment = 'left'; //El segundo [] es el numero de columna a alinear
                  doc.content[1].table.body[i][4].alignment = 'right';
                  doc.content[1].table.body[i][3].alignment = 'right';
                  doc.content[1].table.body[i][6].alignment = 'center';
                  doc.content[1].table.body[i][2].alignment = 'center';
                }; // Arnold deja de copiarme
                //Es equivalente a: doc.content[0].table.widths = ['*', '*', '*', '*', '*', '*'];
						// Change dataTable layout (Table styling)
						// To use predefined layouts uncomment the line below and comment the custom lines below
						// doc.content[0].layout = 'lightHorizontalLines'; // noBorders , headerLineOnly
						var objLayout = {};
						objLayout['hLineWidth'] = function(i) { return .5; };
						objLayout['vLineWidth'] = function(i) { return .5; };
						objLayout['hLineColor'] = function(i) { return '#aaa'; };
						objLayout['vLineColor'] = function(i) { return '#aaa'; };
						objLayout['paddingLeft'] = function(i) { return 4; };
						objLayout['paddingRight'] = function(i) { return 4; };
						doc.content[1].layout = objLayout;
				}}
        ],
        columnDefs: [
            { 'sortable': true, 'searchable': false, 'visible': false, 'type': 'num', 'targets': [0] }
        ],
        order: [
            [0, "desc"]
        ],
        language: {
            sProcessing: "Procesando...",
            sLengthMenu: "Mostrar _MENU_ registros",
            sZeroRecords: "No se encontraron resultados",
            sEmptyTable: "Ningún dato disponible en esta tabla",
            sInfo: "Mostrando _START_ al _END_ de un total de _TOTAL_ registros",
            sInfoEmpty: "Mostrando registros del 0 al 0 de un total de 0 registros",
            sInfoFiltered: "(filtrado de un total de _MAX_ registros)",
            sInfoPostFix: "",
            sSearch: "Buscar:",
            sUrl: "",
            sInfoThousands: ",",
            sLoadingRecords: "Cargando...",
            oPaginate: {
                sFirst: "Primero",
                sLast: "Último",
                sNext: "Siguiente",
                sPrevious: "Anterior"
            },
            oAria: {
                "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                "sSortDescending": ": Activar para ordenar la columna de manera descendente"
            },
            buttons: {
                "copy": "Copiar",
                "colvis": "Visibilidad"
            }
        },
    });
    $('#midtbusqueda').keyup(function() {
      midatatable.search($(this).val()).draw();
    })
  $.fn.dataTableExt.afnFiltering.push(
              function(oSettings, aData, iDataIndex) {
                  var iFini = document.getElementById('min').value;
                  var iFfin = document.getElementById('max').value;
                  var iStartDateCol = 3;
                  var iEndDateCol = 3;
                  console.log(aData[3]);
                  iFini = iFini.substring(6, 10) + iFini.substring(3, 5) + iFini.substring(0, 2);
                  iFfin = iFfin.substring(6, 10) + iFfin.substring(3, 5) + iFfin.substring(0, 2);

                  var datofini = aData[iStartDateCol].substring(6, 10) + aData[iStartDateCol].substring(3, 5) + aData[iStartDateCol].substring(0, 2);
                  var datoffin = aData[iEndDateCol].substring(6, 10) + aData[iEndDateCol].substring(3, 5) + aData[iEndDateCol].substring(0, 2);

                  if (iFini === "" && iFfin === "") {
                      return true;
                  } else if (iFini <= datofini && iFfin === "") {
                      return true;
                  } else if (iFfin >= datoffin && iFini === "") {
                      return true;
                  } else if (iFini <= datofini && iFfin >= datoffin) {
                      return true;
                  }
                  return false;
              }
          );

          $('#min').daterangepicker({
                  changeMonth: true,
                  changeYear: true,
                  singleDatePicker: true,
                  locale: {
                      format: 'DD/MM/YYYY',
                      applyLabel: 'Submit',
                      cancelLabel: 'Clear',
                      fromLabel: 'From',
                      toLabel: 'To',
                      customRangeLabel: 'Custom',
                      daysOfWeek: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
                      monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
                      firstDay: 1
                  }
              },
              function(start, end, label) {
                  console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
              });

          $('#max').daterangepicker({

              changeMonth: true,
              changeYear: true,
              singleDatePicker: true,
              locale: {
                  format: 'DD/MM/YYYY',
                  applyLabel: 'Submit',
                  cancelLabel: 'Clear',
                  fromLabel: 'From',
                  toLabel: 'To',
                  customRangeLabel: 'Custom',
                  daysOfWeek: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
                  monthNames: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
                  firstDay: 1
              }

          });
          $('#min').val('');
          $('#max').val('');
          var table = $('#midatatable').DataTable();

          // Event listener to the two range filtering inputs to redraw on input
          $('#min, #max').change(function() {
              table.draw();
          });

      });

      // In your Javascript (external .js resource or <script> tag)
$(document).ready(function() {
    $('.js-example-basic-single').select2();
});
$(document).ready(function() {
    $('.js-example-basic-multiple').select2();
});


// combito
$('#combito').change(function() {
    var mt = $(this).val();
    $.ajax({
        url: '/prenda/mostrar_unidad',
        data: {
            'material': mt
        },
        dataType: 'json',
        success: function(result) {
            var html = "";

              html +=  result['medida'];

              $("#unidad_medida").html(html);

        }
    })
});
