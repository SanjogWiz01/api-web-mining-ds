import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Concurrency {

    public static void main(String[] args) throws Exception {
        ExecutorService executor = Executors.newFixedThreadPool(8);
        HttpClient client = HttpClient.newBuilder().executor(executor).build();

        List<String> urls = List.of(
                "https://api.example.com/v1/a",
                "https://api.example.com/v1/b",
                "https://api.example.com/v1/c",
                "https://api.example.com/v1/d");

        List<CompletableFuture<HttpResponse<String>>> futures = urls.stream()
                .map(url -> HttpRequest.newBuilder().uri(URI.create(url)).GET().build())
                .map(req -> client.sendAsync(req, HttpResponse.BodyHandlers.ofString()))
                .toList();

        CompletableFuture.allOf(futures.toArray(new CompletableFuture[0])).join();

        for (CompletableFuture<HttpResponse<String>> future : futures) {
            HttpResponse<String> response = future.get();
            System.out.println(response.uri() + " -> " + response.statusCode());
        }

        executor.shutdown();
    }
}