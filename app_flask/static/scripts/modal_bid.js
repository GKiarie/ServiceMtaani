$(document).on("click", ".bidForJob", function () {
    console.log("Hello World");
    var jobId = $(this).data('id');
    $(".modal-body #job_id").val( jobId );
    $('.bidForJob').hide();
    
    
    // console.log(jobId);
    
    // As pointed out in comments, 
    // it is unnecessary to have to manually call the modal.
    // $('#addBookDialog').modal('show');
});

$(document).on("click", ".submitbutton", function () {
    $('.bidForJob').hide();
});