package com.example.demo.models;

public class WeatherCriteria {
	private String maximum;
	private String year;
	public String getYear() {
		return year;
	}
	public void setYear(String year) {
		this.year = year;
	}
	public String getMaximum() {
		return maximum;
	}
	public void setMaximum(String maximum) {
		this.maximum = maximum;
	}
	public String getMinimum() {
		return minimum;
	}
	public void setMinimum(String minimum) {
		this.minimum = minimum;
	}
	public String getMonth() {
		return month;
	}
	public void setMonth(String month) {
		this.month = month;
	}
	public String getDay() {
		return day;
	}
	public void setDay(String day) {
		this.day = day;
	}
	public String getType() {
		return type;
	}
	public void setType(String type) {
		this.type = type;
	}
	private String type;

	private String minimum;
	private String month;
	private String day;
	
}


