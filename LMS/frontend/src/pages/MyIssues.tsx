import React, { useEffect, useState } from 'react';
import { bookIssueService } from '../services/api';
import { Button } from '../components/ui/button';
import { toast } from 'react-hot-toast';

interface BookIssue {
  id: number;
  book_title: string;
  status: string;
  issue_date: string;
  due_date: string;
  return_date: string;
  reissue_count: number;
}

const MyIssues: React.FC = () => {
  const [issues, setIssues] = useState<BookIssue[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [refreshTrigger, setRefreshTrigger] = useState<number>(0);

  useEffect(() => {
    const fetchIssues = async () => {
      setIsLoading(true);
      try {
        const data = await bookIssueService.getMyIssues();
        setIssues(data);
      } catch (error) {
        console.error('Error fetching issues:', error);
        toast.error('Failed to load your book issues');
      } finally {
        setIsLoading(false);
      }
    };

    fetchIssues();
  }, [refreshTrigger]);

  const handleReissue = async (issueId: number) => {
    try {
      await bookIssueService.reissueBook(issueId);
      toast.success('Book reissued successfully');
      setRefreshTrigger(prev => prev + 1);
    } catch (error) {
      console.error('Error reissuing book:', error);
      toast.error('Failed to reissue book');
    }
  };

  if (isLoading) {
    return <div className="p-8 text-center">Loading your book issues...</div>;
  }

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">My Books</h1>
      
      {issues.length === 0 ? (
        <div className="bg-white shadow-md rounded-lg p-6 text-center">
          <p className="text-gray-500">You don't have any book issues yet.</p>
          <p className="mt-2">Browse the books catalog to request a book.</p>
        </div>
      ) : (
        <div className="bg-white shadow-md rounded-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Book</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Issue Date</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
                  <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {issues.map((issue) => (
                  <tr key={issue.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{issue.book_title}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span 
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                        ${issue.status === 'ISSUED' ? 'bg-green-100 text-green-800' : 
                          issue.status === 'REQUESTED' ? 'bg-yellow-100 text-yellow-800' : 
                          issue.status === 'OVERDUE' ? 'bg-red-100 text-red-800' : 
                          issue.status === 'RETURNED' ? 'bg-gray-100 text-gray-800' :
                          'bg-gray-100 text-gray-800'}`}
                      >
                        {issue.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {issue.issue_date ? new Date(issue.issue_date).toLocaleDateString() : '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {issue.due_date ? new Date(issue.due_date).toLocaleDateString() : '-'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      {issue.status === 'ISSUED' && issue.reissue_count < 3 && (
                        <Button
                          onClick={() => handleReissue(issue.id)}
                          variant="outline"
                          size="sm"
                          className="text-blue-600 hover:text-blue-900"
                        >
                          Reissue
                        </Button>
                      )}
                      {issue.status === 'OVERDUE' && issue.reissue_count < 3 && (
                        <Button
                          onClick={() => handleReissue(issue.id)}
                          variant="outline"
                          size="sm"
                          className="text-blue-600 hover:text-blue-900"
                        >
                          Reissue
                        </Button>
                      )}
                      {(issue.status === 'ISSUED' || issue.status === 'OVERDUE') && issue.reissue_count >= 3 && (
                        <span className="text-xs text-gray-500">Max reissues reached</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default MyIssues; 