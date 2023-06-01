$(document).ready(function() {
        $("#accept_bid").click(function() {
            // Prepare the data to send
            var bidId = $(this).data("bid-id");
            // console.log("Bid ID: " + bidId);
            var data = {
                // Add your data properties here
                bid_id: bidId
            };

            // Send an AJAX PUT request to your Flask server
            $.ajax({
                url: "/client",  // Replace with your Flask route
                method: "PUT",
                data: JSON.stringify(data),
                contentType: "application/json",
                success: function(response) {
                    // Handle the success response
                    console.log("Data sent successfully");
                },
                error: function(xhr, status, error) {
                    // Handle the error response
                    console.error("Error sending data:", error);
                }
            });
        });
    });
