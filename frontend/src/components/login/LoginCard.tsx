import * as React from "react";
import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "../ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "../ui/card";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { AuthContext } from "../../contexts/AuthContext";

export default function LoginCard() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [university, setUniversity] = useState("");
  const authContext = useContext(AuthContext);
  const navigate = useNavigate();

  if (!authContext) {
    throw new Error("AuthContext must be used within an AuthProvider");
  }

  const { login } = authContext;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Mock API call
    const response = await fakeApiLogin(username, password, university);
    if (response.token) {
      login(response.token);
      navigate("/");
    } else {
      console.error("Login failed");
    }
  };

  return (
    <Card className="w-[350px]">
      <CardHeader className="mb-5">
        <CardTitle>
          <div className="flex justify-center items-center gap-2">
            <img
              src={`${process.env.PUBLIC_URL}/logo.svg`}
              alt="logo"
              className="w-9 aspect-square"
            />
            <h2 className="font-bold text-3xl">Student Scheduler</h2>
          </div>
        </CardTitle>
        <CardDescription>The only friend you can count on</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="university">Choose your university</Label>
              <Select onValueChange={setUniversity}>
                <SelectTrigger id="university">
                  <SelectValue placeholder="Select" />
                </SelectTrigger>
                <SelectContent position="popper">
                  <SelectItem value="WUT">Warsaw University of Technology</SelectItem>
                  <SelectItem value="UW">University of Warsaw</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>
          <CardFooter className="flex justify-center items-center mt-4">
            <Button type="submit" className="gap-2">
              <svg
                width="15"
                height="15"
                viewBox="0 0 15 15"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M4.5 1C4.22386 1 4 1.22386 4 1.5C4 1.77614 4.22386 2 4.5 2H12V13H4.5C4.22386 13 4 13.2239 4 13.5C4 13.7761 4.22386 14 4.5 14H12C12.5523 14 13 13.5523 13 13V2C13 1.44772 12.5523 1 12 1H4.5ZM6.60355 4.89645C6.40829 4.70118 6.09171 4.70118 5.89645 4.89645C5.70118 5.09171 5.70118 5.40829 5.89645 5.60355L7.29289 7H0.5C0.223858 7 0 7.22386 0 7.5C0 7.77614 0.223858 8 0.5 8H7.29289L5.89645 9.39645C5.70118 9.59171 5.70118 9.90829 5.89645 10.1036C6.09171 10.2988 6.40829 10.2988 6.60355 10.1036L8.85355 7.85355C9.04882 7.65829 9.04882 7.34171 8.85355 7.14645L6.60355 4.89645Z"
                  fill="currentColor"
                ></path>
              </svg>
              Login using USOS
            </Button>
          </CardFooter>
        </form>
      </CardContent>
    </Card>
  );
}

const fakeApiLogin = async (username: string, password: string, university: string) => {
  return new Promise<{ token?: string }>((resolve) => {
    setTimeout(() => {
      if (username === "user" && password === "pass") {
        resolve({ token: "fake-jwt-token" });
      } else {
        resolve({});
      }
    }, 1000);
  });
};
