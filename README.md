# Learning English App 

Welcome to the Learning English App API documentation. This application primarily serves as an API platform built on Rest Framework, allowing users to access various endpoints for learning English.

## ERD (Entity-Relationship Diagram)

### 1. User learning and course relationships
![Course LearningEnglishApp](https://github.com/TranDatk/LearningEnglishApp-Django/assets/84312661/5adc7be1-7433-4e8b-9cca-09e19a4d4c6c)

### 2. User Infor

![User Learning English App](https://github.com/TranDatk/LearningEnglishApp-Django/assets/84312661/d71a566a-165e-45b7-b897-18638a3c06af)

## API Endpoints

The API provides endpoints for different functionalities:

### Authentication
- **POST /api/auth/login:** Endpoint for user login.
- **POST /api/auth/logout:** Endpoint for user logout.

### Learning Modules
- **GET /api/vocabulary:** Retrieve vocabulary words categorized by topics.
- **GET /api/grammar-lessons:** Access grammar rules and sentence structures.
- **GET /api/listening-practice:** Retrieve audio clips for enhancing listening comprehension.

### Interactive Exercises
- **GET /api/quizzes:** Access quizzes tailored to learning modules.
- **POST /api/speaking-practice:** Practice speaking through interactions with AI-powered chatbots.

### Progress Tracking
- **GET /api/user/progress:** Retrieve user progress statistics.
- **POST /api/user/preferences:** Set personalized learning preferences.

## Swagger Documentation

Explore the API endpoints and interact with them using Swagger UI. Access the Swagger documentation by navigating to:

- **Development:** `http://localhost:8000/swagger/`
- **Production:** `https://yourdomain.com/swagger/`

## Getting Started

To get started with the Learning English App API:

1. **Installation:** Clone the repository and set up the environment.
2. **Dependencies:** Install required dependencies from the `requirements.txt` file.
3. **Run the Server:** Start the server using `python manage.py runserver`.

## Feedback and Support

We value your feedback! If you encounter any issues or have suggestions for improvements, please create an issue on the GitHub repository or contact our support team at trannhatminhdat1103@gmail.com.

## Contributing

Contributions are welcome! If you'd like to contribute to the enhancement of the Learning English App API, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.
