import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;

public class FileUploads {

    public static void main(String[] args) throws Exception {
        HttpClient client = HttpClient.newHttpClient();

        String boundary = "----JavaBoundary" + System.currentTimeMillis();
        Path filePath = Path.of("data.csv");
        String fileContent = "id,name,score\n1,alpha,0.9\n2,beta,0.7\n";

        String body = "--" + boundary + "\r\n"
                + "Content-Disposition: form-data; name=\"file\"; filename=\"" + filePath.getFileName() + "\"\r\n"
                + "Content-Type: text/csv\r\n\r\n"
                + fileContent + "\r\n"
                + "--" + boundary + "--\r\n";

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.example.com/v1/upload"))
                .header("Content-Type", "multipart/form-data; boundary=" + boundary)
                .POST(HttpRequest.BodyPublishers.ofString(body))
                .build();

        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Upload status: " + response.statusCode());
        System.out.println("Server response: " + response.body());
    }
}