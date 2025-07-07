import {useState} from 'react';
import StudentGradeSearch from '../components/StudentGradeSearch';
const GradePage = () => {
  const [activeTab, setActiveTab] = useState('student');
  return (
     <div>
      <div className='container'>
        <h1 className='mt-5'>Grade Management</h1>
        
        {/* Navigation Tab */}
        <ul className="nav nav-tabs mb-4">
          <li className="nav-item">
            <button 
              className={`nav-link ${activeTab === 'student' ? 'active' : ''}`}
              onClick={() => setActiveTab('student')}
            >
              Individual Student Grades
            </button>
          </li>
        </ul>

        {activeTab === 'student' && <StudentGradeSearch />}

      </div>
    </div>
  );
};

export default GradePage