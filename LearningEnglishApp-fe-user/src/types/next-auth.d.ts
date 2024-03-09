import NextAuth, {DefaultSession} from "next-auth";

interface IUser{
    pk: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
}

declare module "next-auth/jwt" {
    interface JWT{
        access_token: string;
        refresh_token: string;
        user: IUser;
    }
}

declare module "next-auth" {
    interface Session{
        access_token: string;
        refresh_token: string;
        user: IUser;
    }
}