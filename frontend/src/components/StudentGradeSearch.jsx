import {useState} from 'react';
import Axios from '../services/Axios';

const StudentGradeSearch = () => {
    const[studentData, setStudentData] = useState([]);
    const[searchId, setSearchId] = useState('');
    const[loading, setLoading] = useState(false);
    const[error, setError] = useState('');

    const searchStudent = async () => {
        if (!searchId.trim()) { // Check if searchId is empty or just spaces
            setError('Please enter a student ID');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const response = await Axios.get('/student_enrollments', {
                params: { student_id_number: searchId }
            });

            if (response.data.length === 0) {
                setError('Student has no course enrollments');
                setStudentData([]);
            } else {
                setStudentData(response.data);
            }
        } catch (err) {
            console.error('Error fetching student grades:', err);
            setError('Student not found or error occurred');
            setStudentData([]);
        } finally {
            setLoading(false);
        }
    }
  return (
    <div>
        <h3>Search Student Grades</h3>

        <div className = 'row mb-6'>
            <div className='col-md-6 '>
                <div className='input-group'>
                    <input 
                        type='text' 
                        className='form-control' 
                        placeholder='Enter Student ID Number' 
                        value={searchId} 
                        onChange={(e) => {
                            setSearchId(e.target.value);
                            setError(''); // Clear error on new input when user types
                        }}

                        onKeyDown={(e) => e.key === 'Enter' && searchStudent()}
                    />

                    <button 
                        className='btn btn-primary'
                        onClick={searchStudent}
                        disabled={loading}>
                            {loading ? 'Searching...' : 'Search'}
                    </button>
                </div>
            </div>
        </div>
    

    {error && (
        <div className='alert alert-danger' role='alert'>
            {error}
        </div>
    )}
    {studentData.length > 0 && (
        <div>
            <h4 className='mb-3 mt-5'>
                Grades for {studentData[0].student_name}, {studentData[0].student_id_number}
            </h4>

            <table className='table table-striped table-bordered'>
                <thead>
                    <tr>
                        <th>Course Name</th>
                        <th>Course Number</th>
                        <th>Credits</th>
                        <th>Teacher</th>
                        <th>Grade</th>
                    </tr>
                </thead>
                <tbody>
                    {studentData.map((enrollment, index) => (
                        <tr key={`${enrollment.course_number}-${index}`}>
                            <td>{enrollment.course_name}</td>
                            <td>{enrollment.course_number}</td>
                            <td>{enrollment.credits}</td>
                            <td>{enrollment.teacher}</td>
                            <td>{enrollment.grade}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
 
    )}
    </div>
  );
}

export default StudentGradeSearch