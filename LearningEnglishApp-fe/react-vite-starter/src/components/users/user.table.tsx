import { useEffect, useState } from 'react';
import '../../styles/users.css'
import { getListUsers, login } from '../../api/user.api';

interface IUser {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    avatar: string;
    email: string;
    is_superuser: boolean;
    is_active: boolean;
}

const UserTable = () => {
    const [listUsers, setListUsers] = useState([])

    useEffect(() => {
        login("admin", "Admin@123")
        getListUsers().then(value => {
            setListUsers(value?.results ?? [])
        }).catch(err => {
            console.log(err);
        });
    }, [])

    console.log(listUsers)

    return (
        <>
            <h2>Table users</h2>
            <table>
                <thead>
                    <tr>
                        <th>Id</th>
                        <th>Username</th>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Email</th>
                        <th>Avatar</th>
                        <th>Admin</th>
                        <th>Active</th>
                    </tr>
                </thead>
                <tbody>
                    {listUsers.map((value: IUser) => {
                        return (
                            <tr key={value?.id}>
                                <td>{value?.id}</td>
                                <td>{value?.username}</td>
                                <td>{value?.first_name}</td>
                                <td>{value?.last_name}</td>
                                <td>{value?.email}</td>
                                <td>{value?.avatar}</td>
                                <td>{value?.is_superuser.toString()}</td>
                                <td>{value?.is_active.toString()}</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </>
    )
}

export default UserTable;