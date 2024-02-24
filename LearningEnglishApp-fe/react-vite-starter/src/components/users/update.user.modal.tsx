import {
    Modal, Form, Input, Switch, Button,
} from 'antd';
import { IUser } from './user.table';
import { registerUser } from '../../api/user.api';
import { useEffect } from 'react';

interface IState {
    isModalOpen: boolean;
    setIsModalOpen: (isModalOpen: boolean) => void;
    setIsAddSuccess: (isAddSuccess: boolean) => void;
    dataUpdate: IUser | null;
}

const UpdateUserModal = (state: IState) => {
    const [form] = Form.useForm<IUser>();

    state.setIsAddSuccess(false);

    const handleOk = () => {
        registerUser(form.getFieldsValue()).then((value) => {
            if (!!value) {
                state.setIsAddSuccess(true)
            }
        })
        state.setIsModalOpen(false);
    };

    useEffect(() => {
        form.setFieldValue("username", state.dataUpdate?.username)
        form.setFieldValue("first_name", state.dataUpdate?.first_name)
        form.setFieldValue("last_name", state.dataUpdate?.last_name)
        form.setFieldValue("email", state.dataUpdate?.email)
        form.setFieldValue("is_superuser", state.dataUpdate?.is_superuser)
    }, [state.dataUpdate])

    return (
        <Modal
            maskClosable={false}
            title="Sửa thông tin người dùng"
            open={state.isModalOpen}
            onOk={handleOk}
            onCancel={() => state.setIsModalOpen(false)}
            footer={[
                <Button key="back" onClick={() => state.setIsModalOpen(false)}>
                    Hủy
                </Button>,
                <Button key="submit" htmlType='submit' type="primary" onClick={handleOk}>
                    Xong
                </Button>,
            ]}>
            <Form
                labelCol={{ span: 5 }}
                wrapperCol={{ span: 15 }}
                layout="horizontal"
                style={{ maxWidth: 600 }}
                form={form}
                onFinish={handleOk}
            >
                <Form.Item label="Username" name="username" rules={[{ required: true }]}>
                    <Input
                        id="username"
                        value={state?.dataUpdate?.username ?? ""}
                        onChange={(e) => { form.setFieldValue("username", e.target.value) }} />
                </Form.Item>
                <Form.Item label="Firstname" name="first_name" rules={[{ required: true }]}>
                    <Input
                        value={state?.dataUpdate?.first_name ?? ""}
                        onChange={(e) => { form.setFieldValue("first_name", e.target.value) }} />
                </Form.Item>
                <Form.Item label="Lastname" name="last_name" rules={[{ required: true }]}>
                    <Input
                        value={state?.dataUpdate?.last_name ?? ""}
                        onChange={(e) => { form.setFieldValue("last_name", e.target.value) }} />
                </Form.Item>
                <Form.Item label="Email" name="email" rules={[{ required: true }]}>
                    <Input
                        value={state?.dataUpdate?.email ?? ""}
                        onChange={(e) => { form.setFieldValue("email", e.target.value) }} />
                </Form.Item>
                <Form.Item label="is_superuser" name="is_superuser" valuePropName="checked" rules={[{ required: true }]}>
                    <Switch
                        checked={state?.dataUpdate?.is_superuser ?? false}
                        onChange={(e) => { form.setFieldValue("is_superuser", e) }} />
                </Form.Item>
            </Form>
        </Modal >
    )
}

export default UpdateUserModal;