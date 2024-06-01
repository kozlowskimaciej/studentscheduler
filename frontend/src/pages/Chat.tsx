import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import Navbar from "../components/common/Navbar";

// Define keyframes for animation
const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

// Styled components
const Card = styled.div`
  width: 90%;
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  animation: ${fadeIn} 0.3s ease-in-out;
`;

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  max-height: 500px;
  overflow: hidden;
`;

const Messages = styled.div`
  flex: 1;
  padding: 10px;
  overflow-y: auto;
`;

const ChatBubbleStyled = styled.div<{ isUser: boolean }>`
  margin: 5px 0;
  padding: 10px;
  border-radius: 10px;
  max-width: 80%;
  background-color: ${(props) => (props.isUser ? '#007bff' : '#f1f0f0')};
  color: ${(props) => (props.isUser ? 'white' : 'black')};
  align-self: ${(props) => (props.isUser ? 'flex-end' : 'flex-start')};
  word-break: break-word;
  overflow-wrap: break-word;
`;

const InputContainer = styled.div`
  display: flex;
  border-top: 1px solid #ccc;
`;

const Input = styled.input`
  flex: 1;
  padding: 10px;
  border: none;
  border-radius: 0 0 0 10px;
  outline: none;
`;

const Button = styled.button`
  padding: 10px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 0 0 10px 0;
  cursor: pointer;

  &:hover {
    background-color: #0056b3;
  }
`;

const SubjectList = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 20px;
`;

const SubjectButton = styled.button<{ isActive: boolean }>`
  padding: 10px 20px;
  margin: 0 5px;
  border: none;
  background-color: ${(props) => (props.isActive ? '#007bff' : '#f1f0f0')};
  color: ${(props) => (props.isActive ? 'white' : 'black')};
  border-radius: 5px;
  cursor: pointer;

  &:hover {
    background-color: #0056b3;
    color: white;
  }
`;

// Define the interface for ChatBubbleProps
interface ChatBubbleProps {
  text: string;
  isUser: boolean;
  sender: string;
}

// Define ChatBubble component with explicit prop types using the ChatBubbleProps interface
const ChatBubble: React.FC<ChatBubbleProps> = ({ text, isUser, sender }) => (
  <ChatBubbleStyled isUser={isUser}>
    <strong>{sender}:</strong> {text}
  </ChatBubbleStyled>
);

// Define the type for the message object
interface Message {
  text: string;
  isUser: boolean;
  sender: string;
}

// Define the type for the chat object
interface Chat {
  subject: string;
  messages: Message[];
}

const mockFetchSubjectsAndChats = async () => {
  // This function simulates fetching data from a database
  return [
    {
      subject: 'Math',
      messages: [
        { text: 'Hello Math', isUser: true, sender: 'User' },
        { text: 'Hi there!', isUser: false, sender: 'Bot' }
      ]
    },
    {
      subject: 'Science',
      messages: [
        { text: 'Hello Science', isUser: true, sender: 'User' },
        { text: 'Hi there!', isUser: false, sender: 'Bot' }
      ]
    }
  ];
}

export default function Calendar() {
  const [chats, setChats] = useState<Chat[]>([]);
  const [currentInput, setCurrentInput] = useState<{ [key: string]: string }>({});
  const [currentSubject, setCurrentSubject] = useState<string>('');

  useEffect(() => {
    const fetchData = async () => {
      const data = await mockFetchSubjectsAndChats();
      setChats(data);
      if (data.length > 0) {
        setCurrentSubject(data[0].subject);
      }
    }
    fetchData();
  }, []);

  const handleSend = (subject: string) => {
    if (currentInput[subject]?.trim()) {
      const newMessage = { text: currentInput[subject], isUser: true, sender: 'User' };
      setChats(prevChats =>
        prevChats.map(chat =>
          chat.subject === subject
            ? { ...chat, messages: [...chat.messages, newMessage] }
            : chat
        )
      );
      setCurrentInput(prevInput => ({ ...prevInput, [subject]: '' }));
    }
  };

  const handleInputChange = (subject: string, value: string) => {
    if (value.length <= 500) {
      setCurrentInput(prevInput => ({ ...prevInput, [subject]: value }));
    }
  };

  const handleSubjectSelect = (subject: string) => {
    setCurrentSubject(subject);
  };

  const currentChat = chats.find(chat => chat.subject === currentSubject);

  return (
    <>
      <Navbar />
      <SubjectList>
        {chats.map(chat => (
          <SubjectButton
            key={chat.subject}
            isActive={chat.subject === currentSubject}
            onClick={() => handleSubjectSelect(chat.subject)}
          >
            {chat.subject}
          </SubjectButton>
        ))}
      </SubjectList>
      {currentChat && (
        <Card>
          <h3 style={{ textAlign: 'center' }}>{currentChat.subject}</h3>
          <ChatContainer>
            <Messages>
              {currentChat.messages.map((msg, index) => (
                <ChatBubble key={index} text={msg.text} isUser={msg.isUser} sender={msg.sender} />
              ))}
            </Messages>
            <InputContainer>
              <Input
                type="text"
                value={currentInput[currentChat.subject] || ''}
                onChange={(e) => handleInputChange(currentChat.subject, e.target.value)}
                placeholder="Type a message (max 500 chars)"
              />
              <Button onClick={() => handleSend(currentChat.subject)}>Send</Button>
            </InputContainer>
          </ChatContainer>
        </Card>
      )}
    </>
  );
}
