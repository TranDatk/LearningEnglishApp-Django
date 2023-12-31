import { useEffect, useState } from 'react';
import { getListUsers, login } from '../../api/user.api';
import type { ColumnsType } from 'antd/es/table';
import Table from 'antd/es/table';
import { CheckCircleOutlined, CloseCircleOutlined, EditOutlined, PlusCircleOutlined, DeleteOutlined } from '@ant-design/icons';
import {
    Space, Button, Image
} from 'antd';
import AddUserModal from './user.modal';

export interface IUser {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    avatar: any;
    email: string;
    password1: string;
    password2: string;
    is_superuser: boolean;
    is_active: boolean;
}

const columns: ColumnsType<IUser> = [
    {
        title: 'Id',
        dataIndex: 'id',
        key: 'id',
    },
    {
        title: 'Username',
        dataIndex: 'username',
        key: 'username',
    },
    {
        title: 'Firstname',
        dataIndex: 'first_name',
        key: 'first_name',
    },
    {
        title: 'Lastname',
        dataIndex: 'last_name',
        key: 'last_name',
    },
    {
        title: 'Email',
        dataIndex: 'email',
        key: 'email',
    },
    {
        title: 'Avatar',
        dataIndex: 'avatar',
        key: 'avatar',
        render: (_, { avatar }) => (
            <>
                <Image
                    width={50}
                    src={avatar}
                    style={{ borderRadius: 400 / 2 }}
                />
            </>
        ),
    },
    {
        title: 'is_superuser',
        dataIndex: 'is_superuser',
        key: 'is_superuser',
        render: (_, { is_superuser }) => (
            <>
                {is_superuser && <CheckCircleOutlined style={{ color: 'green' }} />}
                {!is_superuser && <CloseCircleOutlined style={{ color: 'red' }} />}
            </>
        ),
    },
    {
        title: 'is_active',
        dataIndex: 'is_active',
        key: 'is_active',
        render: (_, { is_active }) => (
            <>
                {is_active && <CheckCircleOutlined style={{ color: 'green' }} />}
                {!is_active && <CloseCircleOutlined style={{ color: 'red' }} />}
            </>
        ),
    },
    {
        title: 'Action',
        key: 'action',
        render: () => (
            <Space size="middle">
                <Button onClick={() => { }} type="default" icon={<EditOutlined />} style={{ background: '#F0E68C' }} />
                <Button onClick={() => { }} type="primary" danger icon={<DeleteOutlined />} />
            </Space>
        ),
    },
]

// eslint-disable-next-line @typescript-eslint/no-explicit-any

const UserTable = () => {
    const [listUsers, setListUsers] = useState([])
    const [isAddUserModalOpen, setIsAddUserModalOpen] = useState(false);
    const [isAddSuccess, setIsAddSuccess] = useState(false)

    useEffect(() => {
        login("admin", "Admin@123")
        getListUsers().then((value) => {
            setListUsers(value?.data?.results ?? [])
        }).catch(err => {
            console.log(err);
        });
    }, [isAddSuccess,])

    return (
        <>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <h2>Danh sách người dùng</h2>
                <Button onClick={() => setIsAddUserModalOpen(true)} type="primary" icon={<PlusCircleOutlined />} style={{ background: '#9ACD32', marginTop: '20px', marginRight: '10vw' }}>Thêm mới</Button>
            </div>
            <Table columns={columns} dataSource={listUsers} />
            <AddUserModal isModalOpen={isAddUserModalOpen} setIsModalOpen={setIsAddUserModalOpen} setIsAddSuccess={setIsAddSuccess} />
        </>
    )
}

export default UserTable;