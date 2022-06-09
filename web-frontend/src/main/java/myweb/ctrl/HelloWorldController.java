package myweb.ctrl;

import org.springframework.core.env.Environment;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import mylib.RemlaUtil;

@Controller
public class HelloWorldController {

	private String modelHost;

	private int numPred = 0;
	private int numCorrect = 0;

	public HelloWorldController(Environment env) {
		modelHost = env.getProperty("MODEL_HOST");
	}

	public void addPrediction() {
		numPred++;
	}

	public void addCorrect() {
		numCorrect++;
	}

	@GetMapping("/")
	@ResponseBody
	public String index() {
		var sb = new StringBuilder();
		sb.append("Hello World!<br /><br />");

		sb.append("Model host: ").append(modelHost).append("<br/>");
		sb.append("Hostname: ").append(RemlaUtil.getHostName()).append("<br/>");
		sb.append("Version: ").append(RemlaUtil.getUtilVersion()).append("<br/>");

		return sb.toString();
	}

	@GetMapping(value = "/metrics", produces = "text/plain")
	@ResponseBody
	public String metrics() {
		var sb = new StringBuilder();

		sb.append("# HELP my_random A random number\n");
		sb.append("# TYPE my_random gauge\n");
		sb.append("my_random ").append(Math.random()).append("\n\n");

		sb.append("# HELP num_pred Number of requested predictions\n");
		sb.append("# TYPE num_pred counter\n");
		sb.append("num_pred ").append(numPred).append("\n\n");

		var acc = numPred == 0 ? 0 : numCorrect / (double) numPred;

		sb.append("# HELP acc Accuracy of spam detection\n");
		sb.append("# TYPE acc gauge\n");
		sb.append("acc ").append(acc).append("\n\n");

		return sb.toString();
	}
}