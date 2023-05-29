$(document).on("click", ".bidForJob", function () {
    console.log("Hello World");
    var jobId = $(this).data('id');
    $(".modal-body #formprice").val( jobId );
    var mechId = $(this).data('id2');
    // formData.append("mechanic_id", mechId)
    // formData.append("job_id", jobId)

    console.log(mechId);
    console.log(jobId);
    
    // As pointed out in comments, 
    // it is unnecessary to have to manually call the modal.
    // $('#addBookDialog').modal('show');
});