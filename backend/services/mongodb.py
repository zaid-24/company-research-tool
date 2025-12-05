from datetime import datetime
from typing import Any, Dict, Optional

import certifi
from pymongo import MongoClient


class MongoDBService:
    def __init__(self, uri: str):
        # Use certifi for SSL certificate verification with updated options
        self.client = MongoClient(
            uri,
            tlsCAFile=certifi.where(),
            retryWrites=True,
            w='majority'
        )
        self.db = self.client.get_database('tavily_research')
        self.jobs = self.db.jobs
        self.reports = self.db.reports

    def create_job(self, job_id: str, inputs: Dict[str, Any]) -> None:
        """
        Create a new research job record.
        
        Args:
            job_id: Unique identifier for the job.
            inputs: Dictionary containing input parameters for the research.
        """
        try:
            self.jobs.insert_one({
                "job_id": job_id,
                "inputs": inputs,
                "status": "pending",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
        except Exception as e:
            # In production, we'd log this properly
            print(f"Error creating job in MongoDB: {e}")

    def update_job(self, job_id: str, 
                  status: str = None,
                  result: Dict[str, Any] = None,
                  error: str = None) -> None:
        """
        Update a research job with results or status.
        
        Args:
            job_id: Unique identifier for the job.
            status: New status string (optional).
            result: Result dictionary (optional).
            error: Error message string (optional).
        """
        update_data = {"updated_at": datetime.utcnow()}
        if status:
            update_data["status"] = status
        if result:
            update_data["result"] = result
        if error:
            update_data["error"] = error

        try:
            self.jobs.update_one(
                {"job_id": job_id},
                {"$set": update_data}
            )
        except Exception as e:
            print(f"Error updating job in MongoDB: {e}")

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a job by ID.
        
        Args:
            job_id: Unique identifier for the job.
            
        Returns:
            Dictionary containing job details or None if not found.
        """
        try:
            return self.jobs.find_one({"job_id": job_id})
        except Exception as e:
            print(f"Error retrieving job from MongoDB: {e}")
            return None

    def store_report(self, job_id: str, report_data: Dict[str, Any]) -> None:
        """
        Store the finalized research report.
        
        Args:
            job_id: Unique identifier for the job.
            report_data: Dictionary containing the report content and metadata.
        """
        try:
            self.reports.insert_one({
                "job_id": job_id,
                "report_content": report_data.get("report", ""),
                "references": report_data.get("references", []),
                "sections": report_data.get("sections_completed", []),
                "analyst_queries": report_data.get("analyst_queries", {}),
                "created_at": datetime.utcnow()
            })
        except Exception as e:
            print(f"Error storing report in MongoDB: {e}")

    def get_report(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a report by job ID.
        
        Args:
            job_id: Unique identifier for the job.
            
        Returns:
            Dictionary containing report details or None if not found.
        """
        try:
            return self.reports.find_one({"job_id": job_id})
        except Exception as e:
            print(f"Error retrieving report from MongoDB: {e}")
            return None 