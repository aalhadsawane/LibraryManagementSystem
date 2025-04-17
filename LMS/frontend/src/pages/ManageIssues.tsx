import React, { useEffect, useState } from 'react';
import { bookIssueService } from '../services/api';
import { Button } from '../components/ui/button';
import { toast } from 'react-hot-toast';

interface BookIssue {
  id: number;
  book_title: string;
  user_name: string;
  status: string;
  issue_date: string;
  due_date: string;
  return_date: string;
}

const ManageIssues: React.FC = () => {
  const [issues, setIssues] = useState<BookIssue[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [refreshTrigger, setRefreshTrigger] = useState<number>(0);

  useEffect(() => {
    const fetchIssues = async () => {
      setIsLoading(true);
      try {
        const data = await bookIssueService.getAllIssues();
        setIssues(data);
      } catch (error) {
        console.error('Error fetching issues:', error);
        toast.error('Failed to load book issues');
      } finally {
        setIsLoading(false);
      }
    };

    fetchIssues();
  }, [refreshTrigger]);

  const handleApprove = async (issueId: number) => {
    try {
      await bookIssueService.approveIssue(issueId);
      toast.success('Book issue approved successfully');
      setRefreshTrigger(prev => prev + 1);
    } catch (error) {
      console.error('Error approving issue:', error);
      toast.error('Failed to approve book issue');
    }
  };

  const handleReject = async (issueId: number) => {
    try {
      await bookIssueService.rejectIssue(issueId);
      toast.success('Book issue rejected');
      setRefreshTrigger(prev => prev + 1);
    } catch (error) {
      console.error('Error rejecting issue:', error);
      toast.error('Failed to reject book issue');
    }
  };

  const handleReturn = async (issueId: number) => {
    try {
      await bookIssueService.returnBook(issueId);
      toast.success('Book marked as returned');
      setRefreshTrigger(prev => prev + 1);
    } catch (error) {
      console.error('Error returning book:', error);
      toast.error('Failed to mark book as returned');
    }
  };

  if (isLoading) {
    return <div className="p-8 text-center">Loading book issues...</div>;
  }

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Manage Book Issues</h1>
      
      <div className="bg-white shadow-md rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Book</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Member</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Issue Date</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {issues.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-4 text-center text-sm text-gray-500">
                    No book issues found
                  </td>
                </tr>
              ) : (
                issues.map((issue) => (
                  <tr key={issue.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{issue.book_title}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{issue.user_name}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span 
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                        ${issue.status === 'ISSUED' ? 'bg-green-100 text-green-800' : 
                          issue.status === 'REQUESTED' ? 'bg-yellow-100 text-yellow-800' : 
                          issue.status === 'OVERDUE' ? 'bg-red-100 text-red-800' : 
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
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                      {issue.status === 'REQUESTED' && (
                        <>
                          <Button
                            onClick={() => handleApprove(issue.id)}
                            variant="outline"
                            size="sm"
                            className="text-green-600 hover:text-green-900"
                          >
                            Approve
                          </Button>
                          <Button
                            onClick={() => handleReject(issue.id)}
                            variant="outline"
                            size="sm"
                            className="text-red-600 hover:text-red-900"
                          >
                            Reject
                          </Button>
                        </>
                      )}
                      {(issue.status === 'ISSUED' || issue.status === 'OVERDUE') && (
                        <Button
                          onClick={() => handleReturn(issue.id)}
                          variant="outline"
                          size="sm"
                          className="text-blue-600 hover:text-blue-900"
                        >
                          Return
                        </Button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ManageIssues; 