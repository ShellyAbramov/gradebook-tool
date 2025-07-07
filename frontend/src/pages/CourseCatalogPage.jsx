import {useState, useEffect} from 'react';
import Axios from '../services/Axios';

const CourseCatalogPage = () => {
    const [courses, setCourses] = useState([]);


    const fetchCourses = async () => {
        try{
        const response = await Axios.get('/courses');
        setCourses(response.data);
        } catch (error) {
            console.error('Error fetching courses:', error);
        }
    };

    useEffect(() => {
      fetchCourses();
    }, []);


 

  return (
    <div>
        <div className='container'>
            <h1 className='mt-5'>Course Catalog</h1>

            {/* check if there are any courses first */}
            {courses.length > 0 ? (
                <table className='table table-striped table-bordered table-hover mt-2'>
                    <thead>
                        <tr>
                            <th scope='col'>Course Name</th>
                            <th scope='col'>Course Number</th>
                            <th scope='col'>Credits</th>
                            <th scope='col'>Teacher</th>
                            <th scope='col'>Students Enrolled</th>
                        </tr>
                    </thead>
                    <tbody>
                        {courses.map((course, index) => (
                            <tr key={course.course_number || index}>
                                <td>{course.course_name}</td>
                                <td>{course.course_number}</td>
                                <td>{course.credits}</td>
                                <td>{course.teacher}</td>
                                <td>{course.number_of_students}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <p>No courses found.</p>
            )}
        </div>
    </div>
  );
};

export default CourseCatalogPage