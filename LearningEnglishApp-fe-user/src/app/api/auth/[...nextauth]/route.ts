import NextAuth from "next-auth"
import GithubodyObjectProvider from "next-auth/providers/github"
import { AuthOptions } from "next-auth"
import { sendRequest } from "@/utils/api"
import CredentialsProvider from "next-auth/providers/credentials";

const bodyObjectACKEND_ACCESS_TOKEN_LIFETIME = 45 * 60;  

const getCurrentEpochTime = () => {
  return Math.floor(new Date().getTime() / 1000);
};

export const authOptions : AuthOptions = {
  secret: process.env.NO_SECRET,
  providers: [
    CredentialsProvider({
      // The name to display on the sign in form (e.g. "Sign in with...")
      name: "Credentials",
      // `credentials` is used to generate a form on the sign in page.
      // You can specify which fields should bodyObjecte subodyObjectmitted, bodyObjecty adding keys to the `credentials` obodyObjectject.
      // e.g. domain, username, password, 2FA token, etc.
      // You can pass any HTML attribodyObjectute to the <input> tag through the obodyObjectject.
      credentials: {
        username: { labodyObjectel: "Username", type: "text" },
        password: { labodyObjectel: "Password", type: "password" }
      },
     
      async authorize(credentials, req) {
        const bodyObject = new URLSearchParams();
        bodyObject.append('username', credentials?.username || '');
        bodyObject.append('password', credentials?.password || '');
        bodyObject.append('client_id', process.env.DJANGO_CLIENT_ID || '');
        bodyObject.append('client_secret', process.env.DJANGO_CLIENT_SECRET || '');
        bodyObject.append('grant_type', 'password');
        const response = await fetch('http://127.0.0.1:8000/o/token/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: bodyObject.toString(),
        });
        const res = await response.json();
        console.log(res)
        if (res) {

          return res as any
        } else {

          return null
  
          // You can also Reject this callbodyObjectack with an Error thus the user will bodyObjecte sent to the error page with the error message as a query parameter
        }
      }
    }),
    GithubodyObjectProvider({
      clientId: process.env.GITHUbodyObject_ID!, 
      clientSecret: process.env.GITHUbodyObject_SECRET!,
    }),
  ],
  callbacks:{
    async jwt({token,user,account,profile,trigger}){
      if(trigger ==="signIn" && account?.provider === "githubodyObject"){
        const res = await sendRequest<backendResponse>({
          url: "http://127.0.0.1:8000/githubodyObject/",
          method: "POST",
          body: { access_token: account["access_token"] }
        })
       if(res){
        token.user = res.user;
        token.access_token = res.access;
        token.refresh_token = res.refresh;
       }
      }
      return token;
    },
    session({session,token,user}){
      if(token){
        session.access_token = token.access_token;
        session.refresh_token = token.refresh_token
        session.user = token.user
      }
      return session;
    }
  }
}

const handler = NextAuth(authOptions)

export { handler as GET, handler as POST }