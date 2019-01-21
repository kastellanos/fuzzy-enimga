package com.example.demo.controllers;

import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.example.demo.models.WeatherCriteria;
import com.example.demo.producer.Sender;

@Controller
@RequestMapping("/")
public class WeatherController {
	@Autowired
	private Sender sender;
    @GetMapping("/home")
    public String weatherForm(Model model) {
    	model.addAttribute("weatherCriteria", new WeatherCriteria());
        return "criteria2";
        
    }

    @PostMapping("/home")
    public String search(@ModelAttribute WeatherCriteria weather) {
    	 JSONObject obj = new JSONObject();
         obj.put("maximum",weather.getMaximum());
         obj.put("minimum",weather.getMinimum());
         obj.put("year",weather.getYear());
         obj.put("month",weather.getMonth());
         obj.put("day",weather.getDay());
         obj.put("type", weather.getType());
         sender.send(obj.toString());
        return "home";
    }
    
    @GetMapping("")
    public String home(Model model) {
        return "home1";
        
    }
    
    @GetMapping("other")
    public String other(@RequestParam String ville) {
    	JSONObject obj = new JSONObject();
    	obj.put("ville", ville);
    	sender.send(obj.toString());
    	return "results";
    }
    

}
