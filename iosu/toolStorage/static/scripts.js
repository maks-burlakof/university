function showMessage(msgType, HTMLText) {
   if (msgType === 'error') {
      msgType = 'danger';
   }
   let newMsgElem = $('<div>').addClass(`toast mb-1 text-bg-${msgType}`).attr('role', 'alert').attr('aria-live', 'assertive').attr('aria-atomic', 'true');
   newMsgElem.html(`
      <div class="d-flex justify-content-between align-items-center">
         <div class="toast-body">${HTMLText}</div>
         <button type="button" class="btn-close btn-close-white me-3" data-bs-dismiss="toast" aria-label="Закрыть"></button>
      </div>
   `);

   let messagesContainer = $('#messagesContainer');
   messagesContainer.append(newMsgElem);
   bootstrap.Toast.getOrCreateInstance(newMsgElem).show();
   // setTimeout(function () {
   //    newMsgElem.remove();
   // }, 10000);
}

$(document).ready(function() {
   $('.finish-production-button').on('click', function() {
      let productionId = $(this).data('production-id');
      let defectsValue = $(this).parent().find('input').val();
      $.ajax({
         url: '/ajax/finish-production/',
         type: 'POST',
         data: {
            'productionId': productionId,
            'numOfDefects': defectsValue
         },
         success: function(response) {
            if (response.is_success) {
               showMessage('success', 'Изготовление отмечено как выполненное');
               location.reload();
            } else {
               showMessage('error', response.message);
            }
         },
         error: function(error) {
            console.error('Error:', error);
         }
      });
   });

   $('.service-equipment-button').on('click', function() {
      let equipmentId = $(this).data('equipment-id');
      $.ajax({
         url: '/ajax/service-equipment/',
         type: 'POST',
         data: {
            'equipmentId': equipmentId,
         },
         success: function(response) {
            if (response.is_success) {
               showMessage('success', 'Дата последнего обслуживания обновлена');
               location.reload();
            } else {
               showMessage('error', response.message);
            }
         },
         error: function(error) {
            console.error('Error:', error);
         }
      });
   });

   $('.docs-during-button').on('click', function() {
      let docUrl = $(this).data('doc-url');
      let dateFrom = $(this).parent().find('.during-from').val();
      let dateTo = $(this).parent().find('.during-to').val();
      window.open(`${docUrl}?from=${dateFrom}&to=${dateTo}`, '_blank');
   });
});