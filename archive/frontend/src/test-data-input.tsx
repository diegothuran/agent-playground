import React from 'react';
import DataInputModal from '@/components/playground/ChatArea/ChatInput/DataInputModal';

export default function TestDataInput() {
  const handleDataSubmit = (data: string, source: 'file' | 'paste', fileName?: string) => {
    console.log('Data received:', { data, source, fileName });
  };

  return (
    <div className="p-4">
      <h1>Test Data Input</h1>
      <DataInputModal onDataSubmit={handleDataSubmit} />
    </div>
  );
}
