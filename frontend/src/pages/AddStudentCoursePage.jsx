import {useState, useEffect} from 'react';
import Axios from '../services/Axios';

const AddStudentCoursePage = () => {
  const [courses, setCourses] = useState([]);
  const [formData, setFormData] = useState({
    student_id_number: '',
    course_name: '',
    course_number: '',
    credits: '',
    teacher: '',
    grade: ''
  });


    const fetchCourses = async () => {
        const response = await Axios.get('/student_enrollments');
        setCourses(response.data);
        };

    useEffect(() => {
      fetchCourses();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
        ...prevData,
        [name]: value
        }));
    };

    // Saves to PostgreSQL via API
    const handleFormSubmit = async (e) => {
        e.preventDefault();
        try {
        const courseData = {
            student_id_number: formData.student_id_number,
            course_name: formData.course_name,
            course_number: formData.course_number,
            credits: parseInt(formData.credits),
            teacher: formData.teacher,
            grade: parseFloat(formData.grade)
            
        };

      const response = await Axios.post('/add_student_course', courseData);
      console.log("Student's course added:", response.data);

      fetchCourses(); // Refresh the list of courses after adding a new one

      setFormData({
        student_id_number: '',
        course_name: '',
        course_number: '',
        credits: '',
        teacher: '',
        grade: ''
      });
   

    }catch (error) {
      console.error("Error adding student's course:", error);
    }
  };
  return (
    <div>
      <div className='container'>
        <form onSubmit = {handleFormSubmit}>
          <div className ='mb-3 mt-3'>
            <label htmlFor='student_name' className='form-label'>Student Name:</label>
            <input type='text' className='form-control' id='student_name' name='student_name' onChange={handleInputChange} value={formData.student_name} required/>
          </div>
        
          <div className ='mb-3 mt-3'>
            <label htmlFor='student_id_number' className='form-label'>Student ID #:</label>
            <input type='text' className='form-control' id='student_id_number' name='student_id_number' onChange={handleInputChange} value={formData.student_id_number} required/>
          </div>
          <div className ='mb-3 mt-3'>
            <label htmlFor='course_name' className='form-label'>Course Name:</label>
            <input type='text' className='form-control' id='course_name' name='course_name' onChange={handleInputChange} value={formData.course_name}  required/>
          </div>
          <div className ='mb-3 mt-3'>
            <label htmlFor='course_number' className='form-label'>Course Number:</label>
            <input type='text' className='form-control' id='course_number' name='course_number' onChange={handleInputChange} value={formData.course_number}  required/>
          </div>
          <div className ='mb-3 mt-3'>
            <label htmlFor='credits' className='form-label'>Credits:</label>
            <input type='number' className='form-control' id='credits' name='credits' onChange={handleInputChange} value={formData.credits}  required/>
          </div>
          <div className ='mb-3 mt-3'>
            <label htmlFor='teacher' className='form-label'>Teacher:</label>
            <input type='text' className='form-control' id='teacher' name='teacher' onChange={handleInputChange} value={formData.teacher}  required/>
          </div>
          <div className ='mb-3 mt-3'>
            <label htmlFor='grade' className='form-label'>Grade:</label>
            <input type='number' className='form-control' id='grade' name='grade' onChange={handleInputChange} value={formData.grade}  required/>
          </div>

          <button type='submit' className='btn btn-primary'>Submit</button>

        </form>
        {/* for testing purposes below: */}
      <div className='container'>
        <h3 className='mt-5'>Students Courses Added:</h3>
        <table className='table table-striped table-bordered table-hover mt-2'>
          <thead>
            <tr>
              <th scope='col'>Student Name</th>
              <th scope='col'>Student ID #</th>
              <th scope='col'>Course Name</th>
              <th scope='col'>Course Number</th>
              <th scope='col'>Credits</th>
              <th scope='col'>Teacher</th>
              <th scope='col'>Grade</th>
            </tr>
          </thead>


          <tbody>
            {courses.map((course, index) => (
              <tr key={course.student_id_number || index}>
                <td>{course.student_name}</td>
                <td>{course.student_id_number}</td>
                <td>{course.course_name}</td>
                <td>{course.course_number}</td>
                <td>{course.credits}</td>
                <td>{course.teacher}</td>
                <td>{course.grade}</td>
              </tr>
            ))}
          </tbody>

        </table>
      </div>

    </div>
    </div>


        );
}

export default AddStudentCoursePage