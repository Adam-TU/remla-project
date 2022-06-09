package myweb.ctrl;

import java.net.URI;
import java.net.URISyntaxException;

import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import myweb.data.Question;

@Controller
@RequestMapping(path = "/question")
public class QuestionController {

	private String modelHost;

	private RestTemplateBuilder rest;

	private HelloWorldController hw;

	public QuestionController(RestTemplateBuilder rest, Environment env, HelloWorldController hw) {
		this.rest = rest;
		this.hw = hw;
		modelHost = env.getProperty("MODEL_HOST");
	}

	@GetMapping("/")
	public String index(Model m) {
		m.addAttribute("hostname", modelHost);
		return "question/index";
	}

	@PostMapping("/")
	@ResponseBody
	public Question predict(@RequestBody Question question) {
		hw.addPrediction();

		question.result = getPrediction(question);

		if (isCorrect(question.guess, question.result)) {
			hw.addCorrect();
		}

		return question;
	}

	private static boolean isCorrect(String a, String b) {
		a = a.toLowerCase().trim();
		b = b.toLowerCase().trim();
		return a.equals(b);
	}

	private String getPrediction(Question question) {
		try {
			var url = new URI(modelHost + "/predict");
			var c = rest.build().postForEntity(url, question, Question.class);
			return c.getBody().result.trim();
		} catch (URISyntaxException e) {
			throw new RuntimeException(e);
		}
	}
}