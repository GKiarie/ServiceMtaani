$(document).on("click", ".bidForJob", function () {
    var jobId = $(this).data('id');
    $(".modal-body #job_id").val( jobId );
    
    
    // console.log(jobId);
    
    // As pointed out in comments, 
    // it is unnecessary to have to manually call the modal.
    // $('#addBookDialog').modal('show');
});

// $(document).on("click", ".submitbutton", function () {
//     $('.bidForJob').hide();
// });
$(document).on("click", ".editPartDetails", function () {
    var partId = $(this).data('id');
    $("#part_id").val( partId );
});