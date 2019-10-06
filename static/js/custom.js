$(document).ready(function(){

  midatatable = $('#midatatable').DataTable({
        "lengthMenu": [
            [5, 25, 50, -1],
            [5, 25, 50, "All"]
        ],
        dom: 'Brtlip',
        buttons: [
            'copy','csv', 'excel', 'pdf', 'print'
        ],
        'columnDefs': [
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
